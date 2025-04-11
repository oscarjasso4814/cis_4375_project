<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <nav id="navigation">
    <RouterLink to="/" class="logo">Lalani Insurance Agency <span>+LIA</span></RouterLink>
    <ul class="links">
      <li><RouterLink to="/">Home</RouterLink></li>
      <li><RouterLink to="/about">About</RouterLink></li>
      <li class="dropdown">
        <a href="#" class="trigger-drop">Work<i class="arrow"></i></a>
        <ul class="drop">
          <li><RouterLink to="/ex_cust">Ex-Cust</RouterLink></li>
          <li><RouterLink to="/">Drop2</RouterLink></li>
          <li><RouterLink to="/">Drop3</RouterLink></li>
          <li><RouterLink to="/">Drop4</RouterLink></li>
        </ul>
      </li>
      <li class="dropdown">
        <a href="#" class="trigger-drop">Contact<i class="arrow"></i></a>
        <ul class="drop">
          <li><RouterLink to="/contact/email">Email</RouterLink></li>
          <li><RouterLink to="/contact/phone">Phone</RouterLink></li>
        </ul>
      </li>
      <li><RouterLink to="/login">Login</RouterLink></li>
    </ul>
  </nav>
</template>

<style scoped>
/* Base styles */
.content-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Logo in content area */
.content-wrapper .logo {
  display: block;
  margin: auto;
}

/* Navigation styles */
#navigation {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  height: 50px;
  background: #fff;
  box-shadow: 0 0px 9px 4px rgba(0, 0, 0, 0.1), 0 -5px 2px 2px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  min-width: 100%;
}

#navigation .logo {
  position: relative;
  float: left;
  height: 50px;
  line-height: 50px;
  padding: 0 15px;
  font-size: 22px;
  font-weight: 900;
  text-transform: uppercase;
  color: #303052;
  text-decoration: none;
}

#navigation .logo span {
  display: inline-block;
  position: relative;
  top: -8px;
  font-size: 13pt;
}

#navigation .logo:hover {
  background: #c6c6d9;
}

#navigation .links {
  float: right;
  margin-right: 30px;
  position: relative;
  padding: 0;
}

#navigation .links li {
  float: left;
  list-style: none;
  position: relative;
  margin: 10px;
  display: inline-block;
}

#navigation .links li > a {
  position: relative;
  display: inline-block;
  padding: 0 10px;
  line-height: 30px;
  height: 30px;
  color: #303052;
  text-decoration: none;
  font-weight: 600;
}

#navigation .links li > a:hover {
  color: #fff;
  background: #303052;
  border-radius: 2px;
}

#navigation .links li > a[class^="trigger-"] {
  padding-right: 40px;
}

#navigation .links li > a .arrow {
  position: absolute;
  width: 10px;
  height: 10px;
  top: 35%;
  text-align: center;
  right: 10px;
  border-width: 5px 5px 0 5px;
  border-style: solid;
  border-color: rgba(0, 0, 0, 0.3) transparent;
}

#navigation .links li > a .arrow:after {
  content: "";
  border-left: 1px solid rgba(0, 0, 0, 0.15);
  top: -10px;
  left: -15px;
  position: absolute;
  height: 15px;
}

#navigation .links li ul {
  position: absolute;
  left: 0;
  margin: 0;
  background: #fff;
  border-radius: 2px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.15);
  display: none;
  padding: 0;
}

#navigation .links li ul > li {
  clear: both;
  list-style: none;
  display: block;
  padding: 0;
  margin: 0;
  width: 100%;
}

#navigation .links li ul > li:hover {
  background: #c6c6d9;
}

#navigation .links li ul > li:hover > a {
  background: #c6c6d9;
  color: #fff;
}

#navigation .links li ul > li a {
  width: 100%;
  display: block;
}

#navigation .links li:hover > .drop {
  display: block;
  animation: fadeInRight 0.3s ease;
  -webkit-animation: fadeInRight 0.3s ease;
}

@keyframes fadeInRight {
  0% {
    opacity: 0;
    transform: translate3d(100%, 0, 0);
  }
  100% {
    opacity: 1;
    transform: none;
  }
}
</style>