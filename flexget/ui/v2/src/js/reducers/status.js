import { LOADING_STATUS, ERROR_STATUS, CLOSE_STATUS, INFO_STATUS } from 'actions/status';
import { LOCATION_CHANGE } from 'connected-react-router';

const initState = {
  loading: {},
  info: null,
  error: null,
};

export default (state = initState, action) => {
  switch (action.type) {
    case LOADING_STATUS:
      if (state.loading[action.payload.type]) {
        return state;
      }
      return {
        ...state,
        loading: {
          ...state.loading,
          [action.payload.type]: action.payload.namespace,
        },
      };
    case ERROR_STATUS:
      return {
        ...state,
        error: action.payload,

      };
    case INFO_STATUS:
      return {
        ...state,
        info: action.payload.message,
      };
    case CLOSE_STATUS:
    case LOCATION_CHANGE:
      return {
        ...initState,
      };
    default:
      if (state.loading[action.type]) {
        const {
          [action.type]: omit,
          ...loading
        } = state.loading;
        return {
          ...state,
          loading,
        };
      }
      return state;
  }
};
