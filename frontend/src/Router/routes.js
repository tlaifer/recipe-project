import React from "react";
import Search from "../Components/Search";
import Recipe from "../Components/Recipe";
import Favorites from "../Components/Favorites";
import Preferences from "../Components/Preferences";

const routes = [
  {
    path: "/",
    exact: true,
    name: "Search",
    toolbar: () => <p>Search</p>,
    main: () => <Search />,
    inMenu: true
  },
  {
    path: "/favorites",
    name: "Favorites",
    toolbar: () => <p>Favorites</p>,
    main: () => <Favorites />,
    inMenu: true
  },
  {
    path: "/preferences",
    name: "Preferences",
    toolbar: () => <p>Preferences</p>,
    main: () => <Preferences />,
    inMenu: true
  },
  {
    path: "/recipies/:recipeId",
    name: "Recipe",
    toolbar: () => <p>Recipe</p>,
    main: () => <Recipe />,
    inMenu: false
  }
];

export default routes;