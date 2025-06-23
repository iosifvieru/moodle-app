import React, { useEffect } from 'react';

function Logout() {
    useEffect(() => {
        const cookie = localStorage.getItem("authToken")

        if(cookie){
            localStorage.removeItem("authToken")
        }
    });

    return (
        <div>
            <h3>Te-ai deconectat cu succes.</h3>
            <a href="/login">apasa-ma.</a>
        </div>
    )
}

export default Logout;