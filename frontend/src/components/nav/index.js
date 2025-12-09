import Logo from "../../assets/img/logo.svg";

const Nav = () => {
  return (
    <div className="nav">
      <div className="nav__width">
        <img src={Logo} alt="logo" />
        <div className="nav__box">
          <h2>AlgoVision</h2>
          <p>AI-Powered Image processing</p>
        </div>
      </div>
    </div>
  );
};

export default Nav;
