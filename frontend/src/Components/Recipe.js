import React from "react";
import {
  useParams
} from "react-router-dom";

function DisplayRecipe() {
  let { recipeId } = useParams();
  return <h1> Displaying recipe {recipeId}</h1>;
}

class Recipe extends React.Component {
  render() {
    return (
      <DisplayRecipe/>
    )
  }
}

export default Recipe;