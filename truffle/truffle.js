var WalletProvider = require("truffle-wallet-provider");
const Wallet = require('ethereumjs-wallet');
var kovanPrivateKey = new Buffer.from("16d2e5e0047914e2de77eaffa23ff0f0e3934c60429cee9be11b64cb07d2aab6","hex");
var kovanWallet = Wallet.fromPrivateKey(kovanPrivateKey);
var kovanProvider = new WalletProvider(kovanWallet, "https://kovan.infura.io/v3/f4aad1ae148242ee9fae671c041797e8");
module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
  networks: {
    development: {
      host: "127.0.0.1",
      port: 8545,
      network_id: "*", // Match any network id
    },
    kovan: {
      provider: kovanProvider,
      gas: 4600000,
      network_id: 3
    }
  }
};
