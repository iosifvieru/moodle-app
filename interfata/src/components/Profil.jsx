import React, { useState, useEffect } from 'react';
import {jwtDecode} from 'jwt-decode';
import { get_profile } from './api';
import StudentDashboard from './StudentDashboard';

function Profil() {
    const [role, setRole] = useState('');
    const [id, setId] = useState(null);
    const [data, setData] = useState(null);
    const [showLectures, setShowLectures] = useState(false);
    const [url, setUrl] = useState('');

    useEffect(() => {
        const token = localStorage.getItem("authToken");

        if (token) {
            const decoded_token = jwtDecode(token);
            setRole(decoded_token.role);
            setId(decoded_token.sub);

            const fetchProfileData = async () => {
                try {
                    const response = await get_profile();

                    if (decoded_token['role'] === "student") {
                        const student = response.students[0];
                        setData({
                            nume: student.nume,
                            prenume: student.prenume,
                            email: student.email,
                            ciclu_studii: student.ciclu_studii,
                            an_studiu: student.an_studiu,
                            grupa: student.grupa,
                        });
                        setUrl(student._links.lectures.href);
                    }

                    if (decoded_token['role'] === "profesor") {
                        const professor = response.professors[0];
                        setData({
                            nume: professor.nume,
                            prenume: professor.prenume,
                            email: professor.email,
                            grad_didactic: professor.grad_didactic,
                            tip_asociere: professor.tip_asociere,
                            afiliere: professor.afiliere,
                        });
                        setUrl(professor._links.lectures.href);
                    }
                } catch (error) {
                    console.error("Error fetching profile data:", error);
                }
            };

            fetchProfileData();
        }
    }, [id]);

    const handleLectures = () => {
        setShowLectures((prev) => !prev);
    };

    return (
        <div>
            {data ? (
                <div>
                    <h3>{data.nume} {data.prenume}</h3>
                    <p>Email: {data.email}</p>
                    {role === "student" && (
                        <>
                            <p>Ciclu Studii: {data.ciclu_studii}</p>
                            <p>An de Studii: {data.an_studiu}</p>
                            <p>Grupa: {data.grupa}</p>
                        </>
                    )}
                    {role === "profesor" && (
                        <>
                            <p>Grad Didactic: {data.grad_didactic}</p>
                            <p>Tip Asociere: {data.tip_asociere}</p>
                            <p>Afiliere: {data.afiliere}</p>
                        </>
                    )}
                    <button onClick={handleLectures}>
                        {showLectures ? "Hide Lectures" : "View Lectures"}
                    </button>
                </div>
            ) : (
                <p>Loading profile data...</p>
            )}
            {showLectures && url ? (
                <div>
                    <StudentDashboard url={url} />
                </div>
            ) : null}
        </div>
    );
}

export default Profil;
