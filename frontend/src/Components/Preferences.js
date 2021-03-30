import React, {Component} from "react";
import { makeStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';


const submitButtonText = 'Save Changes'
/**
 * TODO: replace with DB call to UserTechniques
 */
let techniques = [
  {
    name: 'tec1',
    value: false
  },
  {
    name: 'tec2',
    value: false
  }
];

/**
 * TODO: replace with DB call to Ingredients & UserIngredients
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

class Preferences extends Component {
  state = {
    techniques: techniques,
    ingredients: ingredients
  };

  handleTechniqueChange = (event) => {
    let index = techniques.findIndex(element => {
      return element.name === event.target.name;
    });
    techniques[index].value = event.target.checked

    this.setState({
      techniques: techniques
    });
  };

  handleIngredientChange = (event, value, reason) => {
    //value will contain the list of currently selected options
    let selectedIngredients = value;

    ingredients.forEach(ingredient => {
      if (selectedIngredients.indexOf(ingredient.name) > -1) {
        ingredient.value = true;
      } else {
        ingredient.value = false
      }
    });
    this.setState({ ingredients: ingredients });
  };

  handleSubmit = () => {
    /**
     * TODO: submit user preferences to server
     */
    return;
  };

  render() {
    return (
      <div className="body">
        <Grid container spacing={3}>
          <Grid item xs>
          </Grid>
          <Grid item xs>
          </Grid>
          <Grid item xs>
            <Button variant="contained" color="primary" onClick={this.handleSubmit}>{submitButtonText}</Button>
          </Grid>
        </Grid>
        <Grid container spacing={3}>
          <FormControl component="fieldset" className="formControl">
            <FormLabel component="legend">What can you do in the kitchen?</FormLabel>
            <FormGroup>
              {this.state.techniques.map(t=>{
                return (
                  <FormControlLabel
                    control={<Checkbox
                      checked={t.value}
                      onChange={this.handleTechniqueChange}
                      name={t.name}
                    />}
                    label={t.name}
                  />
                )
              })}
            </FormGroup>
          </FormControl>
        </Grid>
        <Grid container spacing={3}>
          <Autocomplete className="body"
            multiple
            id="tags-standard"
            style={{ alignContent: "left" }}
            options={this.state.ingredients.map(ingredient => ingredient.name)}
            // defaultValue={[state.ingredients[0].name]}
            getOptionLabel={(option) => option}
            onChange={this.handleIngredientChange}
            renderInput={(params) => (
              <TextField
                {...params}
                variant="standard"
                placeholder="I won't eat..."
              />
            )}
          />
        </Grid>
      </div>
    );
  }
}

export default Preferences;