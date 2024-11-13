export function CustomException(message, status) {
  const error = new Error(message || "Something went wrong!");

  error.code = status || 500;
  return error;
}

export let emptyFormString = 'Not set'
