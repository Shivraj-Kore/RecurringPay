import { useEffect, useState } from 'react';
import Web3 from 'web3';
import abi from '../contract.json'; // Adjust the path as necessary

const contractAddress = '0x0279573897bF717E83244914DC7FdC47dEE8b75C'; // Your TestCoin contract address

export default function HomePage() {
    const [recipient, setRecipient] = useState<string>('');
    const [amount, setAmount] = useState<number | string>('');
    const [status, setStatus] = useState<string>('');

    // Initialize Web3
    const web3 = new Web3(window.ethereum); // Ensure MetaMask is installed

    const handleTransfer = async (event: React.FormEvent) => {
        event.preventDefault();
        if (!recipient || !amount) {
            setStatus('Please fill in all fields.');
            return;
        }

        try {
            // Request user's account
            await window.ethereum.request({ method: 'eth_requestAccounts' });

            // Get the user's account
            const accounts = await web3.eth.getAccounts();
            const senderAddress = accounts[0];

            // Create contract instance
            const contract = new web3.eth.Contract(abi, contractAddress);
            // Transfer tokens
            const transaction = await contract.methods.transfer(recipient, amount).send({ from: senderAddress });

            setStatus(`Transfer successful! Transaction Hash: ${transaction.transactionHash}`);
        } catch (error) {
            console.error(error);
            setStatus('Transfer failed. Check the console for details.');
        }
    };

    return (
        <>
            <h1 className="text-2xl font-bold mb-4">This is the transfer page</h1>
            <form onSubmit={handleTransfer} className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">
                        Recipient Address:
                        <input
                            type="text"
                            value={recipient}
                            onChange={(e) => setRecipient(e.target.value)}
                            required
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </label>
                </div>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">
                        Amount:
                        <input
                            type="number"
                            value={amount}
                            onChange={(e) => setAmount(e.target.value)}
                            required
                            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                    </label>
                </div>
                <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-200">
                    Transfer
                </button>
            </form>

            {status && <p>{status}</p>}
        </>
    );
}
