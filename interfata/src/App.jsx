import Navigation from "./components/Navigation";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import 'bootstrap/dist/css/bootstrap.css';

import Login from "./components/Login";
import Lectures from "./components/Lectures"
import Logout from "./components/Logout";
import Profil from "./components/Profil";
import EditLecture from "./components/EditLecture";
import AddLecture from "./components/AddLecture";
import AddMaterial from "./components/AddMaterial";

function App(){
  
  return (
      <Router>
        <Navigation />
        <Routes>
          <Route path="/" element={<Login />}/>
          <Route path="/courses" element={<Lectures />} />
          <Route path="/profil" element={<Profil />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/edit-lecture/:cod" element={<EditLecture />} />
          <Route path="/add-lecture" element= {<AddLecture />} />
          <Route path="/add-materiale" element={<AddMaterial />} />
        </Routes>
      </Router>
  );
}

export default App;