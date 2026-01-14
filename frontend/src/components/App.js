import "../styles/App.css";
import HomePage from "../pages/homePage";
import Footer from "./footer";
import Nav from "./nav";
import "../assets/footer_style.sass";
import "../assets/nav_style.sass";
import "../assets/home_style.sass";
import "../assets/button_style.sass";

function App() {
  return (
    <div className="container">
      <Nav />
      <HomePage />
      <Footer />
    </div>
  );
}

export default App;
