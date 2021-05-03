import React, {Component} from "react";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Link from '@material-ui/core/Link';
import FavoriteIcon from '@material-ui/icons/Favorite';

import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import axios from 'axios'


const submitButtonText = 'Search'

/**
 * All possible ingredient options
 */
let ingredients = [
  {
    name: 'tomatoes',
    value: false
  },
  {
    name: 'bread',
    value: false
  }
]

/**
 * Test recipe array
 */
let recipes = [
  {
    id: '6057e15ad46859706045d8cc',
    name: 'recipe name',
    ingredients: ['a', 'list', 'of', 'things'],
    techniques: ['a', 'list', 'of', 'things'],
    rating: 4.7,
    cookTime: 35,
    ingredientCount: 5,
    extraCount: 2,
    techniqueCount: 1
  }
];

class Search extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedIngredients: '',
      searchResults: '',
      display: this.props.display,
      currentRecipe: '',
      ingredientList: '',
      ingredientsFetched: false
    }
  };

  handleSearch = () => {
    this.searchApiCall(this.state.selectedIngredients);
    this.setState({ display: 'results' });
  }

  handleRecipeLookup = (recipeId) => {
    this.setState({ currentRecipe: 'results' });
  }

  handleIngredientChange = (event, value, reason) => {
    this.setState({ selectedIngredients: value });
  };

  handleBack = () => {
    this.setState({ display: 'search' })
  }

  handleIngredientLoad = () => {
    if (this.state.ingredientsFetched === false) {
      this.ingredientApiCall()
      this.setState({ ingredientsFetched: true });
    }
  }

  /** searchInput parameter is the collection of ingredients entered by the user */
  searchApiCall = (searchInput) => {
    axios.post('http://sp21-cs411-13.cs.illinois.edu:5000/api/search/', {
      userId: 1, 
      ingredientInput: searchInput
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    }).then((response) => {
      console.log("SUCCESS", response);
      this.setState({ searchResults: response.data.recipeArray });
    }).catch(error => {
      console.log(error)
    });
    return;
  }

  sortApiCall = sortVariableInput => () => {
    axios.post('http://sp21-cs411-13.cs.illinois.edu:5000/api/recipeSort/', {
      sortVariable: sortVariableInput, 
      recipeArray: this.state.searchResults
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    }).then((response) => {
      console.log("SUCCESS", response);
      this.setState({ searchResults: response.data.sortedArray });
    }).catch(error => {
      console.log(error)
    });
    return;
  }

  ingredientApiCall = () => { /** TODO: this should probably be props rather than state */
    axios.get('http://sp21-cs411-13.cs.illinois.edu:5000/api/ingredients/')
    .then((response) => {
      console.log("SUCCESS", response);
      this.setState({ ingredientList: response.data.ingredientArray });
    }).catch(error => {
      console.log(error)
    });
    return;
  }

  saveFavorite = (recipeId) => {
    axios.post('http://sp21-cs411-13.cs.illinois.edu:5000/api/rating/', {
      userId: this.props.userId,
      recipeId: recipeId,
      favorite: 't',
      rating: '',
    }, {
      headers: {
          'Content-Type': 'application/json'
      }
    }).then(response => {
      console.log("SUCCESS", response);
    }).catch(error => {
      console.log(error)
    });
  }

  render() {
    if (this.state.display === 'search') {
      this.handleIngredientLoad()
      return (
        <div className = 'body'>
          <h1> Ready to search for your next meal? </h1>
          <div>
            <Autocomplete
              multiple
              id="tags-standard"
              style={{ alignContent: "left" }}
              options={Array.from(this.state.ingredientList).map(ingredient => ingredient.name)}
              getOptionLabel={(option) => option}
              onChange={(event,value, reason) => this.handleIngredientChange(event, value, reason)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  variant="standard"
                  placeholder="What do you want to cook with today?"
                />
              )}
            />
          </div>
          <div >
            <Button variant="contained" color="primary" onClick={this.handleSearch}>{submitButtonText}</Button>
          </div>
        </div>
      )
    } else {
      return (
        <div className = 'body'>
          <div>
            <Button variant="contained" color="primary" onClick={this.sortApiCall('ingredientCount')}>Sort by Selected Ingredients</Button>
            <Button variant="contained" color="primary" onClick={this.sortApiCall('extraCount')}>Sort by Fewest Extra Ingredients</Button>
            <Button variant="contained" color="primary" onClick={this.sortApiCall('techniqueCount')}>Sort by Preferred Techniques</Button>
          </div>
          <div></div>
          <div>
          <Button variant="contained" color="primary" onClick={this.sortApiCall('cookTime')}>Sort by Cook Time</Button>
          <Button variant="contained" color="primary" onClick={this.sortApiCall('averageRating')}>Sort by Average Rating</Button>
          </div>
          <div></div>
          <Button variant="contained" color="primary" onClick={this.handleBack}>New Search</Button>
          <TableContainer component={Paper}>
            <Table className="table" aria-label="simple table">
              <TableHead>
                <TableRow>
                  <TableCell>Recipe Name</TableCell>
                  <TableCell align="center">Ingredients</TableCell>
                  <TableCell align="center">Techniques</TableCell>
                  <TableCell align="center">Cooking Time</TableCell>
                  <TableCell align="center">Average Rating</TableCell>
                  <TableCell align="center">Specified Ingredients</TableCell>
                  <TableCell align="center">Extra Ingredients</TableCell>
                  <TableCell align="center">Preferred Techniques</TableCell>
                  <TableCell align="right">Add to Favorites</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Array.from(this.state.searchResults).map((row) => (
                  <TableRow key={row.id}>
                    <TableCell component="th" scope="row">
                      <Link onClick={this.handleRecipeLookup} href={"/recipes/" + row.id}>{row.name}</Link>
                    </TableCell>
                    <TableCell align="center">{row.ingredients.join(', ')}</TableCell>
                    <TableCell align="center">{row.techniques.join(', ')}</TableCell>
                    <TableCell align="center">{row.cookTime}</TableCell>
                    <TableCell align="center">{row.averageRating}</TableCell>
                    <TableCell align="center">{row.ingredientCount}</TableCell>
                    <TableCell align="center">{row.extraCount}</TableCell>
                    <TableCell align="center">{row.techniqueCount}</TableCell>
                    <TableCell align="right">
                      <Button onClick={() => {this.saveFavorite(row.id)}}>
                        <FavoriteIcon/>
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </div>
      )
    }
  }
}

export default Search;