import React from 'react';

function ProfessorDetails({ professor, loading }) {
    if (loading) {
        return <p>Loading professor details...</p>;
    }

    return (
        <div>
            <h4>Professor Details:</h4>
            <p>Name: {professor.nume} {professor.prenume}</p>
            <p>Email: {professor.email}</p>
            <p>Grad Didactic: {professor.grad_didactic}</p>
            <p>Tip asociere: {professor.tip_asociere}</p>
            <p>Afiliere: {professor.afiliere}</p>
        </div>
    );
}

export default ProfessorDetails;
