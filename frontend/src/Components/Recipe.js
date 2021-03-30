import React from "react";
import {
  useParams
} from "react-router-dom";


class Recipe extends React.Component {
  state = {
    recipeId: ''
  }

  componentDidMount () {
    const recipeId = this.props.match.params.recipeId
    this.setState({ recipeId: recipeId })
  }

  render() {
    return (
      <h1> Displaying recipe {this.state.recipeId}</h1>
    )
  }
}

export default Recipe;