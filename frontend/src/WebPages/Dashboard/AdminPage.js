import React, { useState, useEffect } from 'react';
import './AdminPage.css';
import axios from 'axios';

const AdminPage = () => {
  //Hooks used throughout the component
  const [recalls, setRecalls] = useState([]);
  const [showEditHistoryModal, setShowEditHistoryModal] = useState(false);
  const [editHistory, setEditHistory] = useState([]);
  const [selectedStates, setSelectedStates] = useState([])
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
  const userName = localStorage.getItem('userName'); 
  const adminID = localStorage.getItem('ID'); 
  const [showRankingsModal, setShowRankingsModal] = useState(false);
  const [companyRankings, setCompanyRankings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);


   // Possible values for dropdown fields
  const categories = ['Egg Products', 'Fully Cooked - Not Shelf Stable', 'Heat Treated - Not Fully Cooked - Not Shelf Stable', 'Heat Treated - Shelf Stable', 'Not Heat Treated - Shelf Stable', 'Products with Secondary Inhibitors - Not Shelf Stable', 'Raw - Intact', 'Raw - Non-Intact', 'Slaughter', 'Thermally Processed - Commercially Sterile', 'Unknown'];
  const classes = ['Class 1', 'Class 2', 'Class 3', 'Public Health Alert'];
  const reasons = ['Import Violation', 'Insanitary Conditions', 'Misbranding', 'Mislabeling', 'Processing Defect', 'Produced Without Benefit of Inspection', 'Product Contamination', 'Unfit for Human Consumption', 'Unreported Allergens'];
  const types = ['Outbreak', 'Public Health Alert', 'Active Recall', 'Closed Recall'];
  const riskLevels = ['High', 'Marginal', 'Low', 'Public Health Alert'];
  const companies = [
    'FakeCompany',
    'Taylor Farms Consumer Line',
    'Chief Operating Officer',
    'General Manager Macgregors Meat Seafood Ltd',
    'Vice President of External Communications',
    'Director FSQA Regulatory Affairs', 
    'Pruski Market'
  ];
  const states = ['Michigan', 'California', 'Texas'];
  
 
//Get and post function that fetches data
  const fetchCompanyRankings = async () => {
    try {
      const response = await axios.get('http://localhost:5000/companyRecalls');
      setCompanyRankings(response.data.details);
      console.log(response.data.details) 
      setShowRankingsModal(true); //Shows the company total recalls
    } catch (error) {
      console.error('Failed to fetch company rankings', error);
    }
  };

  const fetchEditHistory = async (recallNumber) => {
    try {
      const response = await axios.post(`http://localhost:5000/editHistory`, { recall_num: recallNumber });
      if (response.data === 'Not Found' || response.status === 404) {
        // If no entries in manages table for the corresponding recall number
        setEditHistory('No edit history yet.');
      } else if (response.data.details) {
        setEditHistory(response.data.details);
      } else {
        // Default message for any other kind of response
        setEditHistory('Unexpected response format.');
      }
    } catch (error) {
      console.error('Failed to fetch edit history', error);
      setEditHistory('No edit history found!');
    }
    setShowEditHistoryModal(true);
  };

  const RankingsModal = ({ show, onClose, rankings }) => {
    if (!show) {
      return null;
    }
  
    return (
      <div className="modal-backdrop">
        <div className="modal-content">
          <h2>Company Recall Rankings</h2>
          <ul>
            {rankings.map((rank, index) => (
              // rank[0] is the company name and rank[1] is the ranking number
              <li key={index}>{rank[0]} - {rank[1]} recalls</li>
            ))}
          </ul>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    );
  };


  const EditHistoryModal = ({ show, onClose, history }) => {
  if (!show) return null;

  const renderHistoryContent = () => {
    if (typeof history === 'string') {
      return <p>{history}</p>;
    } else if (Array.isArray(history) && history.length > 0) {
      return (
        <ul>
          {history.map((edit, index) => {
            // Dynamically access the last two elements for last edit time and admin ID
            const lastEditTime = edit[edit.length - 2]; // Second to last element
            const adminId = edit[edit.length - 1]; // Last element
            return (
              <li key={index}>
                Last Edit Time: {lastEditTime}, Admin ID: {adminId}
              </li>
            );
          })}
        </ul>
      );
    } else {
      return <p>No edit history yet.</p>;
    }
  };

  return (
    <div className="modal-backdrop">
      <div className="modal-content">
        <h2>Edit History</h2>
        {renderHistoryContent()}
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
};
  

//Fetches every single recall in the entire database and their affected states   
   const fetchRecalls = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/recalls');
      const recallsArray = response.data.details;
      console.log(recallsArray);

      const recallsTransformed = recallsArray.map(recall => ({
        id: recall[0], // Assuming this is a unique identifier for each recall
        recallNumber: recall[0],
        name: recall[1],
        category: recall[2],
        qty: recall[3],
        class: recall[4],
        reason: recall[5],
        year: recall[6],
        riskLevel: recall[7],
        openDate: recall[8],
        type: recall[9],
        company: recall[10],
        closeDate: recall[12],
        affectedStates: recall[13] || 'Not set yet',
      }));

      setRecalls(recallsTransformed);
    } catch (error) {
      console.error('Failed to fetch recalls', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Call fetchRecalls on component mount
  useEffect(() => {
    fetchRecalls();
  }, []); // Empty dependency array ensures this runs once on mount

  const handleAddRecall = async () => {
    const payload = {
      recall_num: newRecall.recallNumber,
      product_name: newRecall.name,
      category: newRecall.category,
      closeDate: newRecall.closeDate,
      qty: parseInt(newRecall.qty, 10),
      class: newRecall.class,
      reason: newRecall.reason,
      year: newRecall.year,
      risklevel: newRecall.riskLevel,
      openDate: newRecall.openDate,
      type: newRecall.type,
      companyID: newRecall.company,
      states: selectedStates,
      admin_id: adminID, // Adjust as needed
    };

    try {
      await axios.post('http://localhost:5000/add', payload);
      alert('Recall added successfully!');
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
        riskLevel: '',
        company: '',
      });
      setSelectedStates([]);

      fetchRecalls(); 
    } catch (error) {
      console.error('Failed to add recall', error);
    }
  };

  const handleEditRecall = async () => {
    const payload = {
      recall_num: newRecall.recallNumber,
      product_name: newRecall.name,
      category: newRecall.category,
      closeDate: newRecall.closeDate,
      qty: parseInt(newRecall.qty, 10),
      class: newRecall.class,
      reason: newRecall.reason,
      year: newRecall.year,
      risklevel: newRecall.riskLevel,
      openDate: newRecall.openDate,
      type: newRecall.type,
      companyID: newRecall.company, 
      states: selectedStates,
      admin_id: adminID, 
    };
  
    try {
      await axios.post('http://localhost:5000/edit', payload);
      alert('Recall edited successfully!');
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
        riskLevel: '',
        company: '',
      });
      setSelectedStates([]);
      fetchRecalls(); 
    } catch (error) {
      console.error('Failed to edit recall', error);
      alert('Failed to edit recall');
    }
  };
 
  const handleStateChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions, option => option.value);
    setSelectedStates(selectedOptions);
  };

  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewRecall({ ...newRecall, [name]: value });
  };

 

  return (
    <div>
  {isLoading ? (
    <p>Loading recalls...</p> 
  ) : (
    <>
      <h2>Admin Page</h2>
      <p>Welcome, {userName}!</p>
      <button onClick={() => fetchCompanyRankings()}>Rankings</button>
      <div>
        <h3>Add Recall</h3>
        <form>
          <input type="text" name="recallNumber" value={newRecall.recallNumber} onChange={handleInputChange} placeholder="Recall Number" required />
          <input type="text" name="name" value={newRecall.name} onChange={handleInputChange} placeholder="Name" required />

          {/* Category Dropdown */}
          <select name="category" value={newRecall.category} onChange={handleInputChange}>
            <option value="">Select Category</option>
            {categories.map((category, index) => (
              <option key={index} value={category}>{category}</option>
            ))}
          </select>

          {/* Class Dropdown */}
          <select name="class" value={newRecall.class} onChange={handleInputChange}>
            <option value="">Select Class</option>
            {classes.map((cls, index) => (
              <option key={index} value={cls}>{cls}</option>
            ))}
          </select>

          {/* Reason Dropdown */}
          <select name="reason" value={newRecall.reason} onChange={handleInputChange}>
            <option value="">Select Reason</option>
            {reasons.map((reason, index) => (
              <option key={index} value={reason}>{reason}</option>
            ))}
          </select>

          {/* Type Dropdown */}
          <select name="type" value={newRecall.type} onChange={handleInputChange}>
            <option value="">Select Type</option>
            {types.map((type, index) => (
              <option key={index} value={type}>{type}</option>
            ))}
          </select>

          {/* Risk Level Dropdown */}
          <select name="riskLevel" value={newRecall.riskLevel} onChange={handleInputChange}>
            <option value="">Select Risk Level</option>
            {riskLevels.map((riskLevel, index) => (
              <option key={index} value={riskLevel}>{riskLevel}</option>
            ))}
          </select>

          <input type="date" name="openDate" value={newRecall.openDate} onChange={handleInputChange} placeholder="Open Date" required />
          <input type="date" name="closeDate" value={newRecall.closeDate} onChange={handleInputChange} placeholder="Close Date" />
          <input type="text" name="qty" value={newRecall.qty} onChange={handleInputChange} placeholder="Quantity" required />
          <input type="text" name="year" value={newRecall.year} onChange={handleInputChange} placeholder="Year" required />

          <select name="company" value={newRecall.company} onChange={handleInputChange}>
            <option value="">Select Company</option>
            {companies.map((companies, index) => (
              <option key={index} value={companies}>{companies}</option>
            ))}
          </select>

          <select multiple name="states" value={selectedStates} onChange={handleStateChange}>
            {states.map((state, index) => (
              <option key={index} value={state}>{state}</option>
            ))}
          </select>
          
          <button type="button" onClick={handleAddRecall}>Add Recall</button>
          <button type="button" onClick={handleEditRecall}>Edit Recall</button>
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
            <th>Company</th>
            <th>States</th>
            <th>Edit</th>
          </tr>
        </thead>
        <tbody>
  {recalls.map(recall => (
    <tr key={recall.id}>
      <td>{recall.recallNumber}</td>
      <td>{recall.name}</td>
      <td>{recall.category}</td>
      <td>{recall.closeDate}</td>
      <td>{recall.qty}</td>
      <td>{recall.class}</td>
      <td>{recall.reason}</td>
      <td>{recall.year}</td>
      <td>{recall.type}</td>
      <td>{recall.openDate}</td>
      <td>{recall.riskLevel}</td>
      <td>{recall.company}</td>
      <td>{recall.affectedStates}</td>
      <td>
      <button onClick={() => fetchEditHistory(recall.recallNumber)}>Edit</button>
      </td>
    </tr>
  ))}
</tbody>
      </table>
      <RankingsModal 
        show={showRankingsModal} 
        onClose={() => setShowRankingsModal(false)} 
        rankings={companyRankings} 
      />
      <EditHistoryModal
      show={showEditHistoryModal}
      onClose={() => setShowEditHistoryModal(false)}
      history={editHistory}
    />
    </>
  )}
</div>
  );
};

export default AdminPage;
 