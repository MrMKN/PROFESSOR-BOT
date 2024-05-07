js
const { Worker } = require('worker_threads');

const worker = new Worker('./bot.py');
worker.on('message', (message) => {
    console.log(message);
});
worker.on('error', (error) => {
    console.error(error);
});
worker.on('exit', (code) => {
    console.log(`Worker exited with code ${code}`);
});
