curl http://repo.varnish-cache.org/debian/GPG-key.txt | sudo apt-key add - &&
echo "deb http://repo.varnish-cache.org/ubuntu/ precise varnish-3.0" | sudo tee -a /etc/apt/sources.list &&
sudo apt-get update &&
sudo apt-get install varnish &&
sudo cp default.vcl /etc/varnish/default.vcl &&
sudo cp varnish /etc/default/varnish
