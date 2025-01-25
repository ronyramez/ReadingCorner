export type RootStackParamList = {
  cart: undefined;
  order: {
    totalPrice: number;
    books: { id: number; title: string; price: number }[];
  };
  // Add other routes here
};
