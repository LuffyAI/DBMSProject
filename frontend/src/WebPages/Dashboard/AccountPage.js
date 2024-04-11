import React, { useState, useEffect } from 'react';
import './AccountPage.css'; 
import axios from 'axios'; 

const states = [
  "California", "Michigan", "Texas"
];

function AccountPage({ userName }) {
  const [selectedStates, setSelectedStates] = useState([]);
  const [recalls, setRecalls] = useState([]);
  const subscriber_id = localStorage.getItem('ID');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

   
    const fetchRecallDetails = async () => {
      if (!subscriber_id) {
          setRecalls([]);
          return;
      }
      
      try {
          const response = await axios.post('http://localhost:5000/subscription_details', { subscriber_id });
          if (response.data && response.data.recalls) {
            console.log(response)  
            setRecalls(response.data.recalls);
          } else {
              setRecalls([]);
          }
      } catch (error) {
          console.error('Failed to fetch recall details', error);
      }
  };

    useEffect(() => {
      // Fetch subscribed states when the component mounts
      const fetchSubscribedStates = async () => {
        try {
          const response = await axios.post('http://localhost:5000/fetchSubbedStates', { subscriber_id });
          if (response.data && response.data.statelist) {
            setSelectedStates(response.data.statelist.map(state => state.StateName));
          }
        } catch (error) {
          console.error('Failed to fetch subscribed states', error);
        }
      };

      fetchSubscribedStates();
      fetchRecallDetails();
    }, [subscriber_id]);


    const handleStateSelection = (state) => {
      const updatedSelection = selectedStates.includes(state)
        ? selectedStates.filter(selectedState => selectedState !== state)
        : [...selectedStates, state];
      setSelectedStates(updatedSelection);
    };
  
   

  useEffect(() => {
    const fetchRecallDetails = async () => {
      try {
        const response = await axios.post('http://localhost:5000/subscription_details', { subscriber_id });
        if (response.data && response.data.recalls) {
          setRecalls(response.data.recalls);
        } else {
          setRecalls([]); // Handle no data scenario
        }
      } catch (error) {
        console.error('Failed to fetch recall details', error);
        // Handle error scenario
      }
    };

    if (subscriber_id) {
      fetchRecallDetails();
    }
  }, [subscriber_id])

  const saveSelection = async () => {
    let hasSubscribedStates = false;

    for (const state of states) {
        if (selectedStates.includes(state)) {
            hasSubscribedStates = true; // At least one state is subscribed
            try {
                await axios.post('http://localhost:5000/subscribe', { subscriber_id, state_name: state });
            } catch (error) {
                console.error(`Failed to subscribe to ${state}`, error);
            }
        } else {
            try {
                await axios.post('http://localhost:5000/unsubscribe', { subscriber_id, state_name: state });
            } catch (error) {
                console.error(`Failed to unsubscribe from ${state}`, error);
            }
        }
    }

    alert('Selections saved!');

    // Only fetch recall details if there are subscribed states, otherwise clear the recalls data
    if (hasSubscribedStates) {
        fetchRecallDetails(); // Refetch recall details after saving selections
    } else {
        setRecalls([]); // Clear recalls data if unsubscribed from all states
    }
};

  
    // Calculate the currently displayed items
    const indexOfLastItem = currentPage * itemsPerPage;
    const indexOfFirstItem = indexOfLastItem - itemsPerPage;
    const currentItems = recalls.slice(indexOfFirstItem, indexOfLastItem);
  
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
            {recalls.length > 0 ? (
                <div className="table-responsive">
                <table>
  <thead>
    <tr>
      <th>Recall Number</th>
      <th>Product Name</th>
      <th>Category</th>
      <th>Close Date</th>
      <th>Quantity</th>
      <th>Class</th>
      <th>Reason</th>
      <th>Year</th>
      <th>Type</th>
      <th>Open Date</th>
      <th>Risk Level</th>
      <th>Company Title</th> {/* Table column headers */}
    </tr>
  </thead>
                    <tbody>
                        {currentItems.map((recall, index) => (
                            <tr key={index}>
                                {/* Data to fill into table columns */}
                                <td>{recall.RecallNum}</td>
                                <td>{recall.ProductName}</td>
                                <td>{recall.Category}</td>
                                <td>{recall.CloseDate}</td>
                                <td>{recall.Qty}</td>
                                <td>{recall.Class}</td>
                                <td>{recall.Reason}</td>
                                <td>{recall.Year}</td>
                                <td>{recall.Type}</td>
                                <td>{recall.OpenDate}</td>
                                <td>{recall.RiskLevel}</td>
                                <td>{recall.CompanyTitle}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                </div>
            ) : (
                <p>No recall details available. Please ensure you are subscribed to notifications.</p>
            )}

            <div className='pagination'>
                {Array.from({ length: Math.ceil(recalls.length / itemsPerPage) }, (_, i) => (
                    <button key={i} onClick={() => paginate(i + 1)}>{i + 1}</button>
                ))}
            </div>
        </div>
    );
}
  
  export default AccountPage;