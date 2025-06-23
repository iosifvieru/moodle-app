import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { formToJSON } from 'axios';
import { ACADEMIA_IP, ACADEMIA_PORT } from './api';

/*
*/
function EditLecture() {
    const { cod } = useParams();
    const [lecture, setLecture] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [formData, setFormData] = useState({
        cod: '',
        id_titular: '',
        nume_disciplina: '',
        an_studiu: '',
        tip_disciplina: '',
        categorie_disciplina: '',
        tip_examinare: '',
    });

    useEffect(() => {
        const fetchLecture = async () => {
            try {
                /* jwt */
                const token = localStorage.getItem('authToken');

                /* request GET catre serviciu cu academia */
                const response = await axios.get(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/lectures/${cod}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    }
                });

                setLecture(response.data.lecture);

                /* completez datele din formular cu cele din raspunsul cererii GET. */
                setFormData({
                    cod: response.data.lecture.cod,
                    id_titular: response.data.lecture.id_titular,
                    nume_disciplina: response.data.lecture.nume_disciplina,
                    an_studiu: response.data.lecture.an_studiu,
                    tip_disciplina: response.data.lecture.tip_disciplina,
                    categorie_disciplina: response.data.lecture.categorie_disciplina,
                    tip_examinare: response.data.lecture.tip_examinare,
                });
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchLecture();
    }, [cod]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({ ...prev, [name]: value }));
    };

    /* face request de tip PUT catre serviciu de materiale */
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            /* jwt */
            const token = localStorage.getItem('authToken');
            
            /* request */ 
            const response = await axios.put(
                `http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/lectures/${cod}`,
                formData,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                }
            );
            alert('Lecture updated successfully!');
        } catch (err) {
            console.error(err);
            alert(`Failed to update lecture: ${err.message}`);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <form onSubmit={handleSubmit}>
            <h2>Edit Lecture: {lecture.nume_disciplina}</h2>

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

export default EditLecture;
