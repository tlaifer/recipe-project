import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Autocomplete from '@material-ui/lab/Autocomplete';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Checkbox from '@material-ui/core/Checkbox';

const useStyles = makeStyles((theme) => ({
  root: {
    padding: "50px 50px 50px 140px",
    textAlign: "left"
  },
  submitButton : {
    textAlign: "right"
  },
  formControl: {
    margin: theme.spacing(3),
  },
}));

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

export default function Preferences() {
  const classes = useStyles();
  const [state, setState] = React.useState({
    techniques: techniques,
    ingredients: ingredients
  });

  const handleTechniqueChange = (event) => {
    let index = techniques.findIndex(element => {
      return element.name === event.target.name;
    });
    state.techniques[index].value = event.target.checked
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  const handleIngredientChange = (event, value, reason) => {
    //value will contain the list of currently selected options
    let selectedIngredients = value;

    ingredients.forEach(ingredient => {
      if (selectedIngredients.indexOf(ingredient.name) > -1) {
        ingredient.value = true;
      } else {
        ingredient.value = false
      }
    });
    setState({ ...state, ingredients: ingredients });
  };

  const handleSubmit = () => {
    /**
     * TODO: submit user preferences to server
     */
    return;
  }

  return (
    <div className={classes.root}>
      <div className={classes.submitButton}>
        <Button variant="contained" color="primary" onClick={handleSubmit}>{submitButtonText}</Button>
      </div>
      <div>
        <FormControl component="fieldset" className={classes.formControl}>
          <FormLabel component="legend">What can you do in the kitchen?</FormLabel>
          <FormGroup>
            {state.techniques.map(t=>{
              return (
                <FormControlLabel
                  control={<Checkbox
                    checked={t.value}
                    onChange={handleTechniqueChange}
                    name={t.name}
                  />}
                  label={t.name}
                />
              )
            })}
          </FormGroup>
        </FormControl>
      </div>
      <div>
        <Autocomplete className={classes.root}
          multiple
          id="tags-standard"
          style={{ alignContent: "left" }}
          options={state.ingredients.map(ingredient => ingredient.name)}
          // defaultValue={[state.ingredients[0].name]}
          getOptionLabel={(option) => option}
          onChange={handleIngredientChange}
          renderInput={(params) => (
            <TextField
              {...params}
              variant="standard"
              placeholder="I won't eat..."
            />
          )}
        />
      </div>
    </div>
  );
}
