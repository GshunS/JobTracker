import React from "react";
import '../style/App.css';

const status = ['APPLYING', 'FIRST_INTERVIEW', 'SECOND_INTERVIEW', 'REJECTED', 'CANCELLED']

const About = () => {
    return (
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

                                    >
                                        Title
                                    </th>
                                    <th className="cell100 column2"

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

                                <tr
                                    className={`row100 body`}
                                >
                                    <td className="cell100 column0">1</td>
                                    <td className="cell100 column1">2</td>
                                    <td className="cell100 column2">3</td>
                                    <td className="cell100 column3">4</td>
                                    <td className="cell100 column4">
                                        <select
                                            className="status"
                                        >
                                            {status.map(st => (
                                                <option key={st} value={st}>
                                                    {st}
                                                </option>
                                            ))}
                                        </select>
                                    </td>
                                </tr>

                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default About;