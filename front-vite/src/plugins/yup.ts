import { setLocale } from 'yup';

setLocale({
  mixed: {
    required: '${path} est un champ requis',
    oneOf: '${path} doit correspond à une de ces valeurs : ${values}',  
  },
  string: {
    email: '${path} doit être un mail valide'
  },
  number: {
    min: '${path} doit être supérieur ou égal à 0'
  }
})