import React, {useState} from "react";
import '../style/insert.css';

const status = ['APPLYING', 'FIRST_INTERVIEW', 'SECOND_INTERVIEW', 'REJECTED', 'CANCELLED']

const About = () => {

    const initialRow = {
        id: 1,
        title: '',
        company: '',
        applied_time: '',
        status: status[0]
    };

    const [rows, setRows] = useState([initialRow]);

    const addRow = () => {
        setRows([...rows, {
            id: rows.length + 1, // Assign a unique ID to each row
            title: '',
            company: '',
            applied_time: '',
            status: status[0] // Set default status
        }]);

    };

    const isValidDate = (dateString) => {
        const regEx = /^\d{4}-\d{2}-\d{2}$/;
        if (!dateString.match(regEx)) return false; // Invalid format
        return true;
    };

    const handleInsert = () => {

        for (const row of rows) {
            if (!row.title || !row.company || !row.applied_time) {
                alert('Please fill in all fields before submitting.');
                return; // Prevent form submission if any field is empty
            }
            if (!isValidDate(row.applied_time)) {
                alert('Invalid date format in applied_time field.');
                return; // Prevent form submission if date format is invalid
            }
        }

        const backendUrl = 'http://localhost:5000';

        // Make a POST request to your Flask backend
        fetch(`${backendUrl}/insert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(rows),
        })
            .then(response => {
                if (!response.ok) {
                    alert('insert failure')
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                alert(data['diff'] + ' records has been inserted');
                window.location.href = 'http://localhost:3000'
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    };


    return (
        <div className="limiter">
            <div className="container-table100">
                <div className="wrap-table100">
                    <div className="table100 ver1 m-b-110">
                        <div className="table100-head">
                            <table>
                                <thead>
                                <tr className="row100 head">
                                    <th className="cell100 column00">Index</th>
                                    <th className="cell100 column01">Title</th>
                                    <th className="cell100 column02">Company</th>
                                    <th className="cell100 column03">Applied_time</th>
                                    <th className="cell100 column04">Status</th>
                                    <th className="cell100 column05" onClick={addRow}>
                                        <strong>+</strong>
                                    </th>
                                </tr>
                                </thead>
                            </table>
                        </div>
                        <div className="table100-body js-pscroll">
                            <table>
                                <tbody>
                                {rows.map((row, index) => (
                                    <tr key={row.id} className={`row100 body`}>
                                        <td className="cell100 column0">{index + 1}</td>
                                        <td className="cell100 column1">
                                            <input
                                                type="text"

                                                placeholder='Type Here'
                                                onChange={(e) => {
                                                    const updatedRows = [...rows];
                                                    updatedRows[index].title = e.target.value;
                                                    setRows(updatedRows);
                                                }}
                                            />
                                        </td>
                                        <td className="cell100 column2">
                                            <input
                                                type="text"

                                                placeholder='Type Here'
                                                onChange={(e) => {
                                                    const updatedRows = [...rows];
                                                    updatedRows[index].company = e.target.value;
                                                    setRows(updatedRows);
                                                }}
                                            />
                                        </td>
                                        <td className="cell100 column3">
                                            <input
                                                type="text"

                                                placeholder='yyyy-mm-dd'
                                                onChange={(e) => {
                                                    const updatedRows = [...rows];
                                                    updatedRows[index].applied_time = e.target.value;
                                                    setRows(updatedRows);
                                                }}
                                            />
                                        </td>
                                        <td className="cell100 column4">
                                            <select
                                                value={row.status}
                                                onChange={(e) => {
                                                    const updatedRows = [...rows];
                                                    updatedRows[index].status = e.target.value;
                                                    setRows(updatedRows);
                                                }}
                                                className="status"
                                            >
                                                {status.map(st => (
                                                    <option key={st} value={st}>
                                                        {st}
                                                    </option>
                                                ))}
                                            </select>
                                        </td>
                                        <td className="cell100 column5"></td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>

                        </div>

                    </div>
                    <table>
                        <tbody>
                        <tr key='submitButton'>
                            <td className="submit"
                                onClick={e => handleInsert()}
                            >
                                Submit
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>

            </div>

        </div>
    );
};

export default About;