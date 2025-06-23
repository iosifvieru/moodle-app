
import './Navigation.css'
import React, { useState, useEffect } from 'react';
import {jwtDecode} from 'jwt-decode';

function Navigation() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [role, setRole] = useState('');

    useEffect(() => {
        const token = localStorage.getItem("authToken")

        if (token) {
            setIsLoggedIn(true);

            const decoded_token = jwtDecode(token)
            setRole(decoded_token.role)
        }
    }, []);

    /* afisez unele link uri in functie de rolul din token, idk daca i bine */
    return (
        <nav>
            {!isLoggedIn && <a href="/">Login</a>}
            
            {isLoggedIn && (role=="profesor")  && <a href="/professor">Professor Dashboard</a>}
            {isLoggedIn && (role=="profesor") && <a href="/add-materiale">Adauga materiale</a>}

            {isLoggedIn && (role=="student" || role=="admin") && <a href="/courses">Courses</a>}
            
            {isLoggedIn && (role!="admin") && <a href="/profil">View Profile</a>}
            {isLoggedIn && role == "admin" && <a href="/add-lecture">Add Lecture</a>}
            {isLoggedIn && <a href="/logout">Logout</a>}
        </nav>
    );
}

export default Navigation;