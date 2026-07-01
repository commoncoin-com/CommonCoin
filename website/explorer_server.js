const express = require('express');
const http = require('http');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 8081;

// Parse commoncoin.conf for RPC credentials
let rpcUser = 'commoncoinrpc';
let rpcPassword = 'rpc_secure_password_replace_me';
let rpcPort = 33556;

const confPath = '/home/ubuntu/.commoncoin/commoncoin.conf';
if (fs.existsSync(confPath)) {
    const lines = fs.readFileSync(confPath, 'utf8').split('\n');
    lines.forEach(line => {
        const parts = line.split('=');
        if (parts.length === 2) {
            const key = parts[0].trim();
            const val = parts[1].trim();
            if (key === 'rpcuser') rpcUser = val;
            if (key === 'rpcpassword') rpcPassword = val;
            if (key === 'rpcport') rpcPort = parseInt(val, 10);
        }
    });
}

function callRpc(method, params = []) {
    return new Promise((resolve, reject) => {
        const payload = JSON.stringify({
            jsonrpc: '1.0',
            id: 'explorer',
            method: method,
            params: params
        });

        const auth = Buffer.from(`${rpcUser}:${rpcPassword}`).toString('base64');
        const req = http.request({
            hostname: '127.0.0.1',
            port: rpcPort,
            path: '/',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': payload.length,
                'Authorization': `Basic ${auth}`
            }
        }, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                if (res.statusCode !== 200) {
                    return reject(new Error(`RPC error: ${res.statusCode} - ${data}`));
                }
                try {
                    const parsed = JSON.parse(data);
                    if (parsed.error) return reject(parsed.error);
                    resolve(parsed.result);
                } catch (e) {
                    reject(e);
                }
            });
        });

        req.on('error', reject);
        req.write(payload);
        req.end();
    });
}

// Serve website assets as static resources
app.use(express.static(path.join(__dirname)));

app.get('/api/status', async (req, res) => {
    try {
        const info = await callRpc('getblockchaininfo');
        res.json(info);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.get('/api/latest_blocks', async (req, res) => {
    try {
        const info = await callRpc('getblockchaininfo');
        const height = info.blocks;
        const blocks = [];
        for (let i = 0; i < 10 && (height - i) >= 0; i++) {
            const hash = await callRpc('getblockhash', [height - i]);
            const block = await callRpc('getblock', [hash]);
            blocks.push({
                height: block.height,
                hash: block.hash,
                txs: block.tx.length,
                time: block.time,
                difficulty: block.difficulty
            });
        }
        res.json(blocks);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.get('/api/block/:param', async (req, res) => {
    try {
        let hash = req.params.param;
        if (/^\d+$/.test(hash)) {
            // It's a block height, look up hash first
            hash = await callRpc('getblockhash', [parseInt(hash, 10)]);
        }
        const block = await callRpc('getblock', [hash]);
        res.json(block);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

app.get('/api/tx/:txid', async (req, res) => {
    try {
        const raw = await callRpc('getrawtransaction', [req.params.txid, true]);
        res.json(raw);
    } catch (e) {
        res.status(500).json({ error: e.message });
    }
});

// Serve explorer.html for /explorer route
app.get('/explorer', (req, res) => {
    res.sendFile(path.join(__dirname, 'explorer.html'));
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`Explorer running on http://0.0.0.0:${PORT}`);
});
