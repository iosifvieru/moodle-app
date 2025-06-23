import React from 'react';
import { MATERIALS_IP, MATERIALS_PORT } from './api';

function MaterialItem({ materials, loading}) {
    if (loading) {
        return <p>Loading materials...</p>;
    }

    if (!materials || Object.keys(materials).length === 0) {
        return <p>No materials found.</p>;
    }

    const getFullUrl = (file) => {
        if (file.startsWith('./')) {
            file = file.substring(2);
        }
        return `http://${MATERIALS_IP}:${MATERIALS_PORT}/${file}`;
    };

    return (
        <div>
            <h4>Materials:</h4>
            <ul>
                {/* Materiale Curs */}
                {materials.materiale_curs && materials.materiale_curs.length > 0 && (
                    <li>
                        <h5>Materiale Curs:</h5>
                        <ul>
                            {materials.materiale_curs.map((file, index) => (
                                <li key={index}>
                                    <a href={getFullUrl(file)} target="_blank" rel="noopener noreferrer">
                                        {file}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </li>
                )}

                {/* Materiale Laborator */}
                {materials.materiale_laborator && materials.materiale_laborator.length > 0 && (
                    <li>
                        <h5>Materiale Laborator:</h5>
                        <ul>
                            {materials.materiale_laborator.map((file, index) => (
                                <li key={index}>
                                    <a href={getFullUrl(file)} target="_blank" rel="noopener noreferrer">
                                        {file}
                                    </a>
                                </li>
                            ))}
                        </ul>
                    </li>
                )}

                {/* Other Materials */}
                {materials.probe_ponderi && (
                    <li>
                        <h5>Probe Ponderi:</h5>
                        <p>{materials.probe_ponderi}</p>
                    </li>
                )}
            </ul>
        </div>
    );
}

export default MaterialItem;
