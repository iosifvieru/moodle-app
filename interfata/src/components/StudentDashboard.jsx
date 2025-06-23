import React, { useState, useEffect } from 'react';
import LectureItem from './LectureItem';
import {jwtDecode} from 'jwt-decode';
import axios from 'axios';
import { ACADEMIA_PORT, ACADEMIA_IP } from './api';

function StudentDashboard({ url }) {
    const [lectures, setLectures] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [role, setRole] = useState(null);

    useEffect(() => {
        const fetchLectures = async () => {
            setLoading(true);
            setError(null);

            const token = localStorage.getItem('authToken');

            try {
                const decodedToken = jwtDecode(token);
                setRole(decodedToken.role);

                const response = await axios.get(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}${url}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });

                const data = response.data;
                let lecturesArray = [];

                if (Array.isArray(data.lectures)) {

                    lecturesArray =
                        decodedToken.role === 'student'
                            ? data.lectures.map((lecture) => lecture.disciplinaID) 
                            : data.lectures; 
                } else if (typeof data.lectures === 'object') {
                    
                    lecturesArray = Object.values(data.lectures);
                    if (decodedToken.role === 'student') {
                        lecturesArray = lecturesArray.map((lecture) => lecture.disciplinaID);
                    }
                } else {
                    throw new Error('Unexpected lectures format');
                }

                setLectures(lecturesArray);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchLectures();
    }, [url]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            <ul>
                {lectures.length > 0 ? (
                    lectures.map((lecture, index) => (
                        <LectureItem
                            key={lecture.cod || index}
                            lecture={lecture}
                        />
                    ))
                ) : (
                    <p>No lectures found.</p>
                )}
            </ul>
        </div>
    );
}

export default StudentDashboard;
