import React, { useState } from 'react';
import axios from 'axios';
import { ACADEMIA_IP, ACADEMIA_PORT } from './api';

/*
adauga o disciplina
*/
function AddLecture() {
    const [formData, setFormData] = useState({
        cod: '',
        id_titular: '',
        nume_disciplina: '',
        an_studiu: '',
        tip_disciplina: '',
        categorie_disciplina: '',
        tip_examinare: '',
    });

    const [error, setError] = useState(null);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            /* token jwt */
            const token = localStorage.getItem('authToken');

            /* request POST catre serviciu academia */
            const response = await axios.post(
                `http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/lectures`,
                formData,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            alert('Lecture added successfully!');
        } catch (err) {
            console.error(err);
            setError(err.message);
            alert(`Failed to add lecture: ${err.message}`);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Add New Lecture</h2>

            {error && <div style={{ color: 'red' }}>Error: {error}</div>}

            <label>
                Cod:
                <input
                    type="text"
                    name="cod"
                    value={formData.cod}
                    onChange={handleInputChange}
                />
            </label>
            <br />

            <label>
                Nume disciplina:
                <input
                    type="text"
                    name="nume_disciplina"
                    value={formData.nume_disciplina}
                    onChange={handleInputChange}
                />
            </label>
            <br />

            <label>
                An studiu:
                <input
                    type="text"
                    name="an_studiu"
                    value={formData.an_studiu}
                    onChange={handleInputChange}
                />
            </label>
            <br />

            <label>
            Categorie disciplina:
            <select
                name="categorie_disciplina"
                value={formData.categorie_disciplina}
                onChange={handleInputChange}
            >
                <option value="0">Domeniu</option>
                <option value="1">Specialitate</option>
                <option value="2">Adiacenta</option>
            </select>
            </label>
            <br />

            <label>
                ID Titular:
                <input
                    type="text"
                    name="id_titular"
                    value={formData.id_titular}
                    onChange={handleInputChange}
                />
            </label>
            <br />

            <label>
                Tip disciplina:
                <select
                    name="tip_disciplina"
                    value={formData.tip_disciplina}
                    onChange={handleInputChange}
                >
                    <option value="0">Impusa</option>
                    <option value="1">Optionala</option>
                    <option value="2">Liber_aleasa</option>
                </select>
            </label>
            <br />

            <label>
                Tip examinare:
                <select
                    name="tip_examinare"
                    value={formData.tip_examinare}
                    onChange={handleInputChange}
                >
                    <option value="0">Examen</option>
                    <option value="1">Colocviu</option>
                </select>
            </label>
            <br />

            <button type="submit">Add Lecture</button>
        </form>
    );
}

export default AddLecture;
