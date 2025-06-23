import React, { useState, useEffect } from 'react';
import { get_professor, get_materials } from './api';
import ProfessorDetails from './ProfessorDetails';
import { jwtDecode } from 'jwt-decode';
import { useNavigate } from 'react-router-dom'; 
import axios from 'axios';
import { ACADEMIA_IP, ACADEMIA_PORT } from './api';
import MaterialItem from './MaterialItem';

function LectureItem({ lecture }) {
    const [selectedProfessor, setSelectedProfessor] = useState(null);
    const [loadingProfessor, setLoadingProfessor] = useState(false);
    const [materials, setMaterials] = useState([]);
    const [loadingMaterials, setLoadingMaterials] = useState(false);
    const [role, setRole] = useState('');
    const [showDetails, setShowDetails] = useState(false);
    const [showMaterials, setShowMaterials] = useState(false);
    const navigate = useNavigate();

    const getIdTitular = (id_titular) => {
        return typeof id_titular === 'object' ? id_titular.id : id_titular;
    };

    useEffect(() => {
        const token = localStorage.getItem('authToken');

        if (token) {
            const decoded_token = jwtDecode(token);
            setRole(decoded_token.role);
        }
    }, []);

    const handleSeeDetails = async (professorId) => {
        if (showDetails) {
            setShowDetails(false);
        } else {
            setLoadingProfessor(true);
            const professorData = await get_professor(professorId);
            setSelectedProfessor(professorData);
            setLoadingProfessor(false);
            setShowDetails(true);
        }
    };

    const handleSeeMaterials = async () => {
        if (showMaterials) {
            setShowMaterials(false);
        } else {
            setLoadingMaterials(true);
            try {
                const materialsData = await get_materials(lecture.cod);
                console.log(materialsData);
                setMaterials(materialsData);
            } catch (error) {
                console.error("Error fetching materials:", error);
            } finally {
                setLoadingMaterials(false);
                setShowMaterials(true);
            }
        }
    };

    const handleEdit = () => {
        navigate(`/edit-lecture/${lecture.cod}`);
    };

    /* request de tip DELETE catre serviciu academia */
    const handleDelete = async () => {
        if (window.confirm(`Are you sure you want to delete lecture "${lecture.nume_disciplina}"?`)) {
            try {
                const token = localStorage.getItem('authToken');
                await axios.delete(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/lectures/${lecture.cod}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                alert('Lecture deleted successfully!');
                window.location.reload();
            } catch (err) {
                console.error(err);
            }
        }
    };

    const professorId = getIdTitular(lecture.id_titular);

    /* 
        returneaza o structura mai complexa:
            - datele despre o disciplina,
            - buton de see details (informatii despre profesorul de la curs).
            - buton de see materials (materialele cursului)
            - buton de edit (doar pentru admin)
            - buton de delete (doar pentru admin)
    */
    return (
        <li>
            <h3>{lecture.nume_disciplina}</h3>
            {role === 'admin' && <p>Cod: {lecture.cod}</p>}
            {role === 'admin' && <p>Profesor titular: {professorId}</p>}
            <p>An de studiu: {lecture.an_studiu}</p>
            <p>Tip disciplina: {lecture.tip_disciplina}</p>
            <p>Categorie disciplina: {lecture.categorie_disciplina}</p>
            <p>Tip examinare: {lecture.tip_examinare}</p>
            
            <button onClick={() => handleSeeDetails(professorId)}>
                {showDetails ? 'Hide Details' : 'See Details'}
            </button>

            <button onClick={handleSeeMaterials}>
                {showMaterials ? 'Hide Materials' : 'Vezi Materiale'}
            </button>

            {showMaterials && (
                <MaterialItem materials={materials} loading={loadingMaterials} />
)           }


            {role === 'admin' && (
                <button onClick={handleEdit}>
                    Edit
                </button>
            )}

            {role === 'admin' && (
                <button onClick={handleDelete}>
                    Delete
                </button>
            )}

            {showDetails && selectedProfessor && selectedProfessor.id === professorId && (
                <ProfessorDetails professor={selectedProfessor} loading={loadingProfessor} />
            )}
        </li>
    );
}

export default LectureItem;
