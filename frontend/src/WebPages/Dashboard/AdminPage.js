import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AdminPage = () => {
  const [recalls, setRecalls] = useState([]);

  useEffect(() => {
    const fetchRecalls = async () => {
      try {
        const response = await axios.get('http://localhost:5000/recalls'); // Replace URL with your backend endpoint
        setRecalls(response.data);
      } catch (error) {
        console.error('Failed to fetch recalls', error);
      }
    };

    fetchRecalls();
  }, []);

  return (
    <div>
      <h2>Admin Page</h2>
      <p>Welcome, {userName}!</p>
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
