#!/bin/bash
set -e

echo "=== 1. Checking Redis Server ==="
sudo systemctl enable redis-server
sudo systemctl restart redis-server
sudo systemctl status redis-server --no-pager

echo "=== 2. Setting up NOMP directory ==="
cd /home/ubuntu
if [ ! -d "/home/ubuntu/nomp" ]; then
    echo "Cloning NOMP repository..."
    git clone https://github.com/zone117x/node-open-mining-portal.git nomp
fi

cd /home/ubuntu/nomp
echo "Installing Node.js dependencies..."
npm install

echo "=== 3. Configuring Pool Settings ==="
# Get a new address for pool fee payouts
POOL_FEE_ADDR=$(commoncoin-cli -conf=/home/ubuntu/.commoncoin/commoncoin.conf getnewaddress "pool_fees")
echo "Generated Pool Fee Address: $POOL_FEE_ADDR"

mkdir -p /home/ubuntu/nomp/pools /home/ubuntu/nomp/pool_configs /home/ubuntu/nomp/coins
cp /home/ubuntu/src/mining-pool/config.json /home/ubuntu/nomp/config.json
cp /home/ubuntu/src/mining-pool/pools/commoncoin.json /home/ubuntu/nomp/pools/commoncoin.json
cp /home/ubuntu/src/mining-pool/pools/commoncoin.json /home/ubuntu/nomp/pool_configs/commoncoin.json
cp /home/ubuntu/src/mining-pool/coins/commoncoin.json /home/ubuntu/nomp/coins/commoncoin.json

# Replace placeholders in pool configuration
sed -i "s/CAddressForPoolFeesGoesHere/$POOL_FEE_ADDR/g" /home/ubuntu/nomp/pools/commoncoin.json
sed -i "s/CAddressForPoolFeesGoesHere/$POOL_FEE_ADDR/g" /home/ubuntu/nomp/pool_configs/commoncoin.json

echo "=== 4. Starting Mining Pool ==="
# Install pm2 to manage node processes
sudo npm install -g pm2
pm2 stop all || true
pm2 start init.js --name "nomp"
pm2 save

echo "NOMP started successfully!"
