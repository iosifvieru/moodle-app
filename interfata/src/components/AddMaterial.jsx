import React, { useState } from 'react';
import axios from 'axios';
import { MATERIALS_PORT, MATERIALS_IP } from './api';

function AddMaterial() {
    const [cod, setCod] = useState('');
    const [materialeCurs, setMaterialeCurs] = useState([]);
    const [materialeLaborator, setMaterialeLaborator] = useState([]);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();

        formData.append('cod', cod);
        materialeCurs.forEach((file) => formData.append('materiale_curs', file));
        materialeLaborator.forEach((file) => formData.append('materiale_laborator', file));

        console.log(formData);

        const token = localStorage.getItem('authToken')
        try {
            const response = await axios.post(`http://${MATERIALS_IP}:${MATERIALS_PORT}/api/materials/upload`, formData, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data'
                }
            });


            //setMessage(response.data.message);
        } catch (error) {
            console.error(error);
            setMessage('An error occurred while uploading files.');
        }
    };

    return (
        <div>
            <h3>Upload Materials</h3>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>Cod:</label>
                    <input
                        type="number"
                        value={cod}
                        onChange={(e) => setCod(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>Materiale Curs:</label>
                    <input
                        type="file"
                        multiple
                        onChange={(e) => setMaterialeCurs(Array.from(e.target.files))}
                    />
                </div>
                <div>
                    <label>Materiale Laborator:</label>
                    <input
                        type="file"
                        multiple
                        onChange={(e) => setMaterialeLaborator(Array.from(e.target.files))}
                    />
                </div>
                <button type="submit">Upload</button>
            </form>
            {message && <p>{message}</p>}
        </div>
    );
}

export default AddMaterial;
