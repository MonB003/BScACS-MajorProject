import './App.css';
import FileCheckForm from './components/FileCheckForm';
import FileUploadForm from './components/FileUploadForm';
import LogGenerator from './components/LogGenerator';

function App() {
  return (
    <div className="App">
     <FileUploadForm />
     <FileCheckForm />
     <LogGenerator />
    </div>
  );
}

export default App; 