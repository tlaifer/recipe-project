import React from "react";
import FavoriteIcon from '@material-ui/icons/Favorite';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';


class Recipe extends React.Component {
  state = {
    recipeId: '',
    rating: '',
    setRating: '',
  }

  componentDidMount () {
    const recipeId = this.props.match.params.recipeId
    this.setState({ recipeId: recipeId })
  }

  handleRadioChange = (event) => {
    this.setState({ rating: event.target.rating });
  };

  handleSubmit = () => {
    /**
     * TODO: rating submit
     */
  };

  render() {
    return (
      <div>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <h1> Recipe Title: recipe {this.state.recipeId}</h1>
        </Grid>
        <Grid item xs={12}>Recipe description</Grid>
        <Grid item xs={6}>Recipe Steps:</Grid>
        <Grid item xs={6}>
          <Grid item xs={6}>
            <Button> Save to Favorites
              <FavoriteIcon/>
            </Button>
          </Grid>
          <Grid item xs={6}>
            <FormControl component="fieldset" >
              <FormLabel component="legend">Rate this recipe!</FormLabel>
              <RadioGroup aria-label="rating" name="rating" value={this.rating} onChange={this.handleRadioChange}>
                <FormControlLabel value="1" control={<Radio />} label="1" />
                <FormControlLabel value="2" control={<Radio />} label="2" />
                <FormControlLabel value="3" control={<Radio />} label="3" />
                <FormControlLabel value="4" control={<Radio />} label="4" />
                <FormControlLabel value="5" control={<Radio />} label="5" />
              </RadioGroup>
              <Button type="submit" variant="outlined" color="primary">
                Submit
              </Button>
            </FormControl>
          </Grid>
          <Grid item xs={6}>
            Other User Ratings
          </Grid>
        </Grid>
      </Grid>
      </div>
    )
  }
}

export default Recipe;