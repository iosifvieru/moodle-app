import React, { useEffect, useState } from "react";
import LectureItem from './LectureItem';
import { get_lectures } from './api';
import { ACADEMIA_IP, ACADEMIA_PORT } from "./api";

function Lectures() {
    const [lectures, setLectures] = useState([]);
    const [paginationLinks, setPaginationLinks] = useState({ next: null, prev: null });
    
    // materiale
    const [materials, setMaterials] = useState([]);

    const fetchLectures = async (url = `http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/lectures?items_per_page=5`) => {
        try {
            /* asteapta rasp. cererii */
            const data = await get_lectures(url);

            if (data && data.lectures) {
                setLectures(Object.values(data.lectures));

                /* hateoas links */
                setPaginationLinks({
                    next: data._links?.next?.href || null,
                    prev: data._links?.prev?.href || null,
                });
            } else {
                console.error("Error: Invalid data structure or no lectures found.");
            }
        } catch (error) {
            console.error("Error fetching lectures:", error);
        }
    };

    useEffect(() => {
        fetchLectures();
    }, []);

    const handleNext = () => {
        if (paginationLinks.next) {
            fetchLectures(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}` + paginationLinks.next);
        }
    };

    const handlePrev = () => {
        if (paginationLinks.prev) {
            fetchLectures(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}` + paginationLinks.prev);
        }
    };

    return (
        <div>
            <h1>Lectures</h1>
            {lectures.length > 0 ? (
                <ul>
                    {lectures.map((lecture, index) => (
                        <LectureItem key={index} lecture={lecture} />
                    ))}
                </ul>
            ) : (
                <p>No lectures found.</p>
            )}
            {materials.length > 0 && (
                <div>
                    <h2>Materials</h2>
                    <ul>
                        {materials.map((material, index) => (
                            <li key={index}>{material}</li>
                        ))}
                    </ul>
                </div>
            )}
            <div>
                <button onClick={handlePrev} disabled={!paginationLinks.prev}>
                    Previous
                </button>
                <button onClick={handleNext} disabled={!paginationLinks.next}>
                    Next
                </button>
            </div>
        </div>
    );
}

export default Lectures;
