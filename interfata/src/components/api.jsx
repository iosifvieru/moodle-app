import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export const LOGIN_API_IP = "10.5.0.6"
export const LOGIN_API_PORT = "8002"

export const ACADEMIA_IP = "10.5.0.2"
export const ACADEMIA_PORT = 8000

export const MATERIALS_IP = "10.5.0.7"
export const MATERIALS_PORT = 8001

export const get_lectures = async (url = `http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/lectures`) => {
    try {
        const token = localStorage.getItem('authToken');
        const response = await axios.get(url, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.error("Error: ", error);
    }
};


export const get_professor = async (id) => {
    try {
        const token = localStorage.getItem('authToken');
        const response = await axios.get(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/professors/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        });
        return response.data.profesor;
    } catch (error) {
        console.error("Eroare: ", error);
    }
};

export const get_student = async(id) => {
    try {
        const token = localStorage.getItem('authToken');

        const response = await axios.get(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/students/${id}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        });
        return response.data;
    } catch (error) {
        console.error("Eroare: ", error);
    }
};

//const decoded_token = jwtDecode(token)
/* 
    face GET parametrizat pe nume si prenume pe serviciu de academie 
*/
export const get_profile = async() => {
    try {
        const token = localStorage.getItem('authToken');
        const decoded_token = jwtDecode(token);

        const email = decoded_token.email;
        console.log(email);

        const info = parseEmail(email);
        console.log(info);

        if(info.rol === "student"){
            const response = await axios.get(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/students?name=${info.nume}&surname=${info.prenume}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });

            console.log(response.data);
            return response.data;
        }

        if(info.rol === "academic"){
            const response = await axios.get(`http://${ACADEMIA_IP}:${ACADEMIA_PORT}/api/academia/professors?name=${info.nume}&surname=${info.prenume}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                }
            });

            console.log(response.data);
            return response.data;
        }

    } catch (error){
        console.error(error);
    }
}

export const get_materials = async (cod) => {
    const token = localStorage.getItem('authToken');
    const response = await axios.get(`http://${MATERIALS_IP}:${MATERIALS_PORT}/api/materials/${cod}`, {
        headers: {
            'Authorization': `Bearer ${token}`,
        }
    });
    return await response.data;
};


/* 
    functie ce parseaza email-ul din token.

    email-ul e de tipul:
    student: iosif.vieru@student.com
    profesor: adrian.doctorul@profesor.com
    admin: aditzza.adminul@admin.com
*/
function parseEmail(email){
    const [numeprenume, domeniu] = email.split('@')
    const [nume, prenume] = numeprenume.split('.')
    const rol = domeniu.split('.')[0];

    return {
        nume,
        prenume,
        rol
    };
}
