import React, { useState } from 'react';
import './AccountPage.css'; 

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
  "Alabama", "Alaska", "Arizona", "Arkansas", "California", 
  "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", 
  "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
  "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
  "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
  "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
  "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
  "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", 
  "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
];

function AccountPage({ userName }) {
    const [selectedStates, setSelectedStates] = useState([]);
  
    const handleStateSelection = (event) => {
      const selectedOptions = Array.from(event.target.selectedOptions, option => option.value);
      setSelectedStates(selectedOptions);
    };
  
    const saveSelection = () => {
      // Placeholder for saving logic
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
  
    return (
      <div className="account-page">
        <div className="account-header">
          <h2>Account Page</h2>
          <p>Welcome, {userName}!</p>
        </div>
        <div className="state-selection-container">
          <label htmlFor="stateSelection" className="label">Choose which states you want to subscribe:</label>
          <select id="stateSelection" multiple={true} value={selectedStates} onChange={handleStateSelection} className="state-select">
            {states.map((state) => (
              <option key={state} value={state}>{state}</option>
            ))}
          </select>
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