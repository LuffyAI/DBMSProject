import React, { useState } from 'react';
import './AccountPage.css'; 
import { useEffect } from 'react'; // Import useEffect here
import axios from 'axios'; // Import axios for making HTTP requests

// NEED TO UPDATE - WHEN NOT SUBSCRIBED TO ANYTHING, SHOW NOTHING IN THE RECALL TABLE, WHEN THE USER
// SUBSCRIBES TO SOMETHING, SHOW THEM THE RECALLS FROM THAT STATE

const mockData = Array.from({ length: 100 }, (_, index) => ({
    recallNumber: `R${index + 1}`,
    name: `Product ${index + 1}`,
    category: `Category ${index % 5 + 1}`,
    closeDate: `2023-0${index % 5 + 1}-12`,
    qty: Math.floor(Math.random() * 100),
    class: `Class ${index % 3 + 1}`,
    reason: `Reason ${index % 4 + 1}`,
    year: 2023,
    type: `Type ${index % 2 + 1}`,
    openDate: `2023-0${index % 5 + 1}-01`,
    riskLevel: `Level ${index % 3 + 1}`
  }));

const states = [
  "California", "Michigan", "Texas"
];

function AccountPage({ userName }) {
    const [selectedStates, setSelectedStates] = useState([]);
    const subscriber_id = localStorage.getItem('ID'); // Corrected this line


    useEffect(() => {
      // Fetch subscribed states when the component mounts
      const fetchSubscribedStates = async () => {
        try {
          const response = await axios.post('http://localhost:5000/fetchSubbedStates', { subscriber_id });
          if (response.data && response.data.statelist) {
            // Assuming response.data.statelist is an array of state names the user is subscribed to
            setSelectedStates(response.data.statelist.map(state => state.StateName));
          }
        } catch (error) {
          console.error('Failed to fetch subscribed states', error);
        }
      };

      fetchSubscribedStates();
    }, [subscriber_id]);


    const handleStateSelection = (state) => {
      const updatedSelection = selectedStates.includes(state)
        ? selectedStates.filter(selectedState => selectedState !== state)
        : [...selectedStates, state];
      setSelectedStates(updatedSelection);
    };
  
     const saveSelection = async () => {
    // Assuming there's a mechanism to get the userId or userName
    for (const state of states) {
      if (selectedStates.includes(state)) {
        // Subscribe to this state
        try {
          await axios.post('http://localhost:5000/subscribe', { subscriber_id, state_name: state });
        } catch (error) {
          console.error(`Failed to subscribe to ${state}`, error);
        }
      } else {
        // Unsubscribe from this state
        try {
          await axios.post('http://localhost:5000/unsubscribe', { subscriber_id, state_name: state });
        } catch (error) {
          console.error(`Failed to unsubscribe from ${state}`, error);
        }
      }
    }
    alert('Selections saved!');
  };
    const [currentPage, setCurrentPage] = useState(1);
    const itemsPerPage = 10; // Set the number of items you want per page
  
    // Calculate the currently displayed items
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = mockData.slice(indexOfFirstItem, indexOfLastItem);
  
    // Change page
    const paginate = pageNumber => setCurrentPage(pageNumber);

      // Retrieve the username from local storage
      userName = localStorage.getItem('userName');

  
    return (
      <div className="account-page">
        <div className="account-header">
          <h2>Account Page</h2>
          <p>Welcome, {userName}!</p>
        </div>
        <div className="state-selection-container">
        <label className="label">Choose which states you want to subscribe:</label>
        <div className="state-checkboxes">
          {states.map((state) => (
            <div key={state} className="state-checkbox">
              <input
                type="checkbox"
                id={state}
                checked={selectedStates.includes(state)}
                onChange={() => handleStateSelection(state)}
              />
              <label htmlFor={state}>{state}</label>
            </div>
          ))}
        </div>
      </div>
        <div>
          <p>Selected States:</p>
          <ul className="state-list">
            {selectedStates.map((state) => (
              <li key={state}>{state}</li>
            ))}
          </ul>
        </div>
        <button onClick={saveSelection} className="btn-save">Save Selection</button>
        <h3>Subscriptions</h3>
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
          </tr>
        </thead>
        <tbody>
          {currentItems.map((item, index) => (
            <tr key={index}>
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
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination */}
      <div className='pagination'>
        {Array.from({ length: Math.ceil(mockData.length / itemsPerPage) }, (_, i) => (
          <button key={i} onClick={() => paginate(i + 1)}>
            {i + 1}
          </button>
        ))}
      </div>
        
      </div>

      
    );
  }
  
  export default AccountPage;