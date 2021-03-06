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

import Button from '@material-ui/core/Button';
import axios from 'axios'

class Favorites extends Component {
    constructor(props) {
      super(props);
  
      this.state = {
        favorites: '',
        display: this.props.display,
        favoritesLoaded : false
      }
    };

    handleLoadFavorites = () => {
        if (this.state.favoritesLoaded === false) {
          this.loadFavorites()
          this.setState({ favoritesLoaded: true });
        }
      }

    loadFavorites = () => {
        axios.get('http://sp21-cs411-13.cs.illinois.edu:5000/api/favorite/', {
          userId: this.props.userId, 
        }, {
          headers: {
              'Content-Type': 'application/json'
          }
        }).then((response) => {
          console.log("SUCCESS", response);
          this.setState({ favorites: response.data.recipeArray });
        }).catch(error => {
          console.log(error)
        });
        return;
    }

    removeFavorite = (recipeId) => {
        if (recipeId == null) {
            return
        }
        axios.delete('http://sp21-cs411-13.cs.illinois.edu:5000/api/favorite/', {
          userId: this.props.userId,
          recipeId: recipeId,
        }, {
          headers: {
              'Content-Type': 'application/json'
          }
        }).then(response => {
          console.log("SUCCESS", response);
        }).catch(error => {
          console.log(error)
        });
        // reload page without causing loop
        // this.setState({ favoritesLoaded: false });
        // this.handleLoadFavorites();
        return


      }

    render() {
        this.handleLoadFavorites()
        return(
            <div className = 'body'>
            <h1> Favorites for User: insert username</h1>
              <TableContainer component={Paper}>
                <Table className="table" aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Recipe Name</TableCell>
                      <TableCell align="center">Ingredients</TableCell>
                      <TableCell align="center">Techniques</TableCell>
                      <TableCell align="center">Cooking Time</TableCell>
                      <TableCell align="center">Average Rating</TableCell>
                      <TableCell align="center">Preferred Techniques</TableCell>
                      <TableCell align="right">Remove from Favorites</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Array.from(this.state.favorites).map((row) => (
                      <TableRow key={row.id}>
                        <TableCell component="th" scope="row">
                          <Link onClick={this.handleRecipeLookup} href={"/recipes/" + row.id}>{row.name}</Link>
                        </TableCell>
                        <TableCell align="center">{row.ingredients.join(', ')}</TableCell>
                        <TableCell align="center">{row.techniques.join(', ')}</TableCell>
                        <TableCell align="center">{row.cookTime}</TableCell>
                        <TableCell align="center">{row.averageRating}</TableCell>
                        <TableCell align="center">{row.techniqueCount}</TableCell>
                        <TableCell align="right">
                          <Button onClick={this.removeFavorite(row.id)}>
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

export default Favorites;
