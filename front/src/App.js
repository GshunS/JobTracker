import './style/App.css';
import React, {useEffect, useState} from 'react';
import {BrowserRouter as Router, Route, Routes} from "react-router-dom"
import InsertPage from './Pages/Insert'
import MainPage from './Pages/mainPage'

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/insert" element={<InsertPage/>}/>
                <Route path="/" element={<MainPage/>}/>
            </Routes>
        </Router>
    );

}

export default App;
