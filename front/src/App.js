import './style/App.css';
import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom"
import InsertPage from './Pages/Insert'

function App() {
    // fetch the data from the backend
    const [data, setData] = useState([]);

    // defind the status
    const status = ['APPLYING', 'FIRST_INTERVIEW', 'SECOND_INTERVIEW', 'REJECTED', 'CANCELLED']

    // orders
    const [orderType, setOrderType] = useState(null);
    const [orderAttr, setOrderAttr] = useState(null);

    // save the updated status
    const [selectedStatus, setSelectedStatus] = useState({});
    const [filterStatus, setFilterStatus] = useState(null);

    const handleStatusChange = (itemId, newStatus) => {
        setSelectedStatus(prevStatus => ({
            ...prevStatus,
            [itemId]: newStatus,
        }));


        sendStatusToBackend(itemId, newStatus);
    };

    useEffect(() => {
        console.log(orderType)
        console.log(orderAttr)
        fetchData();

    }, [orderType]);

    // fetch data from the backend
    const fetchData = async () => {
        try {
            const response = await fetch(
                `http://localhost:5000?filterStatus=${filterStatus}&orderAttr=${orderAttr}&orderType=${orderType}`
            );
            // const response = await fetch('http://192.168.1.67:5000/');
            const result = await response.json();

            setData(result);

        } catch (error) {
            console.error('Error fetching data:', error);
            setData([]);
        }
    };

    // send id and new status to the backend
    const sendStatusToBackend = (itemId, newStatus) => {
        const backendUrl = 'http://localhost:5000';

        // Make a POST request to your Flask backend
        fetch(`${backendUrl}/update_status`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({itemId, newStatus}),
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                window.location.reload();
                return response.json();
            })
            .then(data => {
                console.log('Server response:', data);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    };

    // order title
    const handleTitleClick = (attr) => async () => {
        let newOrder = null;

        // Determine the new order based on the current state
        if (orderType === 'asc') {
            newOrder = 'desc';
        } else if (orderType === 'desc') {
            newOrder = null; // Go back to the original order
        } else {
            newOrder = 'asc';
        }

        // Set the new order
        setOrderType(newOrder);
        setOrderAttr(attr)
    };

    return (
        <Router>
            <Routes>
                <Route path="/insert" element={<InsertPage/>}/>
                <Route path="/" element={
                    <div className="limiter">
                        <div className="container-table100">
                            <div className="wrap-table100">
                                <div className="table100 ver1 m-b-110">
                                    <div className="table100-head">
                                        <table>
                                            <thead>
                                            <tr className="row100 head">
                                                <th className="cell100 column0">Index</th>
                                                <th
                                                    className="cell100 column1"
                                                    onClick={handleTitleClick('title')}
                                                >
                                                    Title
                                                </th>
                                                <th className="cell100 column2"
                                                    onClick={handleTitleClick('company')}
                                                >
                                                    Company
                                                </th>
                                                <th className="cell100 column3">Applied_time</th>
                                                <th className="cell100 column4">Status</th>

                                            </tr>
                                            </thead>
                                        </table>
                                    </div>
                                    <div className="table100-body js-pscroll">
                                        <table>
                                            <tbody>
                                            {data.map((item, index) =>
                                                <tr
                                                    key={item.id}
                                                    className={`row100 body`}
                                                >
                                                    <td className="cell100 column0">{index + 1}</td>
                                                    <td className="cell100 column1">{item.title}</td>
                                                    <td className="cell100 column2">{item.company}</td>
                                                    <td className="cell100 column3">{item.applied_time}</td>
                                                    <td className="cell100 column4">
                                                        <select
                                                            className="status"
                                                            value={selectedStatus[item.id] || item.status}
                                                            onChange={e => handleStatusChange(item.id, e.target.value)}
                                                        >
                                                            {status.map(st => (
                                                                <option key={st} value={st}>
                                                                    {st}
                                                                </option>
                                                            ))}
                                                        </select>
                                                    </td>
                                                </tr>
                                            )}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                }/>

            </Routes>
        </Router>
    );

}


export default App;
