import React, { useState } from 'react';
import './AdminPage.css';
import { useEffect } from 'react'; // Import useEffect here
import axios from 'axios';

// NEED TO FETCH THE RECALLS FROM THE API ENDPOINT TO DISPLAY ALL THE RECALLS TO THE ADMIN
// THE ADMIN CAN VIEW ALL RECALLS, ADD A RECALL, AND EDIT RECALLS

const AdminPage = () => {
  const [recalls, setRecalls] = useState([]);
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
  const userName = localStorage.getItem('userName'); // Retrieve username from localStorage
  const [showRankingsModal, setShowRankingsModal] = useState(false);
  const [companyRankings, setCompanyRankings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);


   // Possible values for dropdown fields
  const categories = ['Egg Products', 'Fully Cooked - Not Shelf Stable', 'Heat Treated - Not Fully Cooked - Not Shelf Stable', 'Heat Treated - Shelf Stable', 'Not Heat Treated - Shelf Stable', 'Products with Secondary Inhibitors - Not Shelf Stable', 'Raw - Intact', 'Raw - Non-Intact', 'Slaughter', 'Thermally Processed - Commercially Sterile', 'Unknown'];
  const classes = ['Class 1', 'Class 2', 'Class 3', 'Public Health Alert'];
  const reasons = ['Import Violation', 'Insanitary Conditions', 'Misbranding', 'Mislabeling', 'Processing Defect', 'Produced Without Benefit of Inspection', 'Product Contamination', 'Unfit for Human Consumption', 'Unreported Allergens'];
  const types = ['Outbreak', 'Public Health Alert', 'Active Recall', 'Closed Recall'];
  const riskLevels = ['High', 'Medium', 'Low'];
  const companies = [
    'FakeCompany',
    'Taylor Farms’ Consumer Line',
    'Chief Operating Officer',
    'General Manager, Macgregors Meat &amp; Seafood Ltd',
    'Vice President of External Communications',
    'Director FSQA &amp; Regulatory Affairs', 
    'Pruski’s Market'
  ];
  const states = ['Michigan', 'California', 'Texas'];
  
  const handleYearChange = (e) => {
    const yearInput = e.target.value;
    // Enforce 4-digit input
    if (/^\d{0,4}$/.test(yearInput)) {
      setNewRecall({ ...newRecall, year: yearInput });
    }
  };

  const fetchCompanyRankings = async () => {
    try {
      const response = await axios.get('http://localhost:5000/companyRecalls');
      setCompanyRankings(response.data.details); // Adjust according to the actual response structure
      console.log(response.data.details)
      setShowRankingsModal(true);
    } catch (error) {
      console.error('Failed to fetch company rankings', error);
    }
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
              // Assuming rank[0] is the company name and rank[1] is the ranking number
              <li key={index}>{rank[0]} - {rank[1]} recalls</li>
            ))}
          </ul>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    );
  };
  

   // Define fetchRecalls outside of useEffect
   const fetchRecalls = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/recalls');
      // Check your actual API response structure and adjust accordingly
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
        closeDate: recall[11],
        affectedStates: recall[12] || 'Not set yet',
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
      admin_id: 3, // Adjust as needed
    };

    try {
      await axios.post('http://localhost:5000/add', payload);
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

      fetchRecalls(); // Refresh recall list
    } catch (error) {
      console.error('Failed to add recall', error);
    }
  };
 
  const handleStateChange = (e) => {
    // Collect all selected options
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
    <p>Loading recalls...</p> // Display loading message
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
        <button>Edit</button>
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
    </>
  )}
</div>
  );
};

export default AdminPage;
  /*
  return (
    <div>
      <h2>Admin Page</h2>
      <p>Welcome, {userName}!</p>
      <button onClick={() => fetchCompanyRankings()}>Rankings</button>
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
          <input type="text" name="Company" value={newRecall.company} onChange={handleInputChange} placeholder="Company" required />
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
        <button>Edit</button>
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
    </div>
  );
};
export default AdminPage;*/

