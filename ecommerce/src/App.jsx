import NavBar from './components/NavBar/NavBar'
import ItemListContainer from './components/ItemListContainer/ItemListContainer'
import './App.css'
function App() {
  return (
    <>
      <NavBar/>
      <ItemListContainer greeting={'Pablo'}/>
      <h1 className="text-3xl font-bold underline">
      Hello world!
    </h1>

    </>
  )
}

export default App

