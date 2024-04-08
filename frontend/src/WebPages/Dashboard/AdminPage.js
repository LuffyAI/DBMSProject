import React, { useState } from 'react';
import './AdminPage.css';
import { useEffect } from 'react'; // Import useEffect here
import axios from 'axios';

const AdminPage = () => {
  const [recalls, setRecalls] = useState([]);
  const [newRecall, setNewRecall] = useState({
    recallNumber: '',
    name: '',
    category: '',
    closeDate: '',
    qty: '',
    class: '',
    reason: '',
    year: '',
    type: '',
    openDate: '',
    riskLevel: ''
  });
  const userName = localStorage.getItem('userName'); // Retrieve username from localStorage

  useEffect(() => {
    const fetchRecalls = async () => {
      try {
        const response = await axios.get('http://localhost:5000/recalls'); // Fetch recalls from the appropriate endpoint
        setRecalls(response.data); // Update recalls state with fetched data
      } catch (error) {
        console.error('Failed to fetch recalls', error);
      }
    };

    fetchRecalls();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewRecall({ ...newRecall, [name]: value });
  };

  const handleAddRecall = async () => {
    try {
      await axios.post('http://localhost:5000/recalls', newRecall); // POST request to add recall
      // After successful addition, fetch recalls again to update the list
      const response = await axios.get('http://localhost:5000/recalls');
      setRecalls(response.data);
      // Clear the new recall form fields
      setNewRecall({
        recallNumber: '',
        name: '',
        category: '',
        closeDate: '',
        qty: '',
        class: '',
        reason: '',
        year: '',
        type: '',
        openDate: '',
        riskLevel: ''
      });
    } catch (error) {
      console.error('Failed to add recall', error);
    }
  };

  return (
    <div>
      <h2>Admin Page</h2>
      <p>Welcome, {userName}!</p>
      <div>
        <h3>Add Recall</h3>
        <form>
          <input type="text" name="recallNumber" value={newRecall.recallNumber} onChange={handleInputChange} placeholder="Recall Number" required />
          <input type="text" name="name" value={newRecall.name} onChange={handleInputChange} placeholder="Name" required />
          <input type="text" name="category" value={newRecall.category} onChange={handleInputChange} placeholder="Category" required />
          <input type="date" name="closeDate" value={newRecall.closeDate} onChange={handleInputChange} placeholder="Close Date" required />
          <input type="text" name="qty" value={newRecall.qty} onChange={handleInputChange} placeholder="Qty" required />
          <input type="text" name="class" value={newRecall.class} onChange={handleInputChange} placeholder="Class" required />
          <input type="text" name="reason" value={newRecall.reason} onChange={handleInputChange} placeholder="Reason" required />
          <input type="text" name="year" value={newRecall.year} onChange={handleInputChange} placeholder="Year" required />
          <input type="text" name="type" value={newRecall.type} onChange={handleInputChange} placeholder="Type" required />
          <input type="date" name="openDate" value={newRecall.openDate} onChange={handleInputChange} placeholder="Open Date" required />
          <input type="text" name="riskLevel" value={newRecall.riskLevel} onChange={handleInputChange} placeholder="Risk Level" required />
          <button type="button" onClick={handleAddRecall}>Add Recall</button>
        </form>
      </div>
      <table>
        <thead>
          <tr>
            <th>Recall#</th>
            <th>Name</th>
            <th>Category</th>
            <th>Close Date</th>
            <th>Qty</th>
            <th>Class</th>
            <th>Reason</th>
            <th>Year</th>
            <th>Type</th>
            <th>Open Date</th>
            <th>Risk Level</th>
            <th>Edit</th>
          </tr>
        </thead>
        <tbody>
          {recalls.map(recall => (
            <tr key={recall.id}>
              <td>{item.recallNumber}</td>
              <td>{item.name}</td>
              <td>{item.category}</td>
              <td>{item.closeDate}</td>
              <td>{item.qty}</td>
              <td>{item.class}</td>
              <td>{item.reason}</td>
              <td>{item.year}</td>
              <td>{item.type}</td>
              <td>{item.openDate}</td>
              <td>{item.riskLevel}</td>
              <td>
                <button onClick={() => handleEdit(recall.id)}>Edit</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminPage;