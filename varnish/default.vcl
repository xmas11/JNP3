# This is a basic VCL configuration file for varnish.  See the vcl(7)
# man page for details on VCL syntax and semantics.
# 
# Default backend definition.  Set this to point to your content
# server.
# 
backend django {
    .host = "127.0.0.1";
    .port = "8000";
    .connect_timeout = 5s;
    .first_byte_timeout = 10s;
    .between_bytes_timeout = 10s;
}
# 
# Below is a commented-out copy of the default VCL logic.  If you
# redefine any of these subroutines, the built-in logic will be
# appended to your code.
sub vcl_recv {
    # unless sessionid/csrftoken is in the request, don't pass ANY cookies (referral_source, utm, etc)  
    if (req.request == "GET" && (req.url ~ "^/static" || (req.http.cookie !~ "sessionid" && req.http.cookie !~ "csrftoken"))) {  
        remove req.http.Cookie;  
    }  
 
    # normalize accept-encoding to account for different browsers  
    # see: https://www.varnish-cache.org/trac/wiki/VCLExampleNormalizeAcceptEncoding  
    if (req.http.Accept-Encoding) {  
        if (req.http.Accept-Encoding ~ "gzip") {  
            set req.http.Accept-Encoding = "gzip";  
        } elsif (req.http.Accept-Encoding ~ "deflate") {  
            set req.http.Accept-Encoding = "deflate";  
        } else {  
            # unkown algorithm  
            remove req.http.Accept-Encoding;  
        }  
    }    
}

sub vcl_pipe {
    # Note that only the first request to the backend will have
    # X-Forwarded-For set.  If you use X-Forwarded-For and want to
    # have it set for all requests, make sure to have:
    # set bereq.http.connection = "close";
    # here.  It is not set by default as it might break some broken web
    # applications, like IIS with NTLM authentication.
    return (pipe);
}

sub vcl_pass {
    return (pass);
}

sub vcl_hash {
    hash_data(req.url);
    if (req.http.host) {
        hash_data(req.http.host);
    } else {
        hash_data(server.ip);
    }
    return (hash);
}

sub vcl_hit {
    return (deliver);
}

sub vcl_miss {
    return (fetch);
}

sub vcl_fetch {  
    # static files always cached  
    if (req.url ~ "^/static") {  
        unset beresp.http.set-cookie;  
        return (deliver);  
    }  
 
    # pass through for anything with a session/csrftoken set  
    if (beresp.http.set-cookie ~ "sessionid" || beresp.http.set-cookie ~ "csrftoken") {
        return (hit_for_pass);  
    } else {  
        return (deliver);  
    }
}  

sub vcl_deliver {
    return (deliver);
}

sub vcl_error {
    set obj.http.Content-Type = "text/html; charset=utf-8";
    set obj.http.Retry-After = "5";
    synthetic {"
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
 "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
  <head>
    <title>"} + obj.status + " " + obj.response + {"</title>
  </head>
  <body>
    <h1>Error "} + obj.status + " " + obj.response + {"</h1>
    <p>"} + obj.response + {"</p>
    <h3>Guru Meditation:</h3>
    <p>XID: "} + req.xid + {"</p>
    <hr>
    <p>Varnish cache server</p>
  </body>
</html>
"};
    return (deliver);
}

sub vcl_init {
	return (ok);
}

sub vcl_fini {
	return (ok);
}
