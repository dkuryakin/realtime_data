import React, {useEffect, useState} from "react";
import './style.scss';
import {useNavigate, useParams} from 'react-router-dom';
import RealtimePlot from "../../components/RealtimePlot";
import Select from 'react-select';

export default function Dashboard() {
    const navigate = useNavigate();
    const {symbol} = useParams();
    const [symbol_, setSymbol_] = useState(symbol || null)
    const [symbols, setSymbols] = useState(null)
    const [symbolsError, setSymbolsError] = useState(false)

    useEffect(() => {
        fetch('/symbols').then(resp => resp.json()).then(resp => {
            setSymbols(resp.map(symbol => ({value: symbol, label: symbol})))
        }).catch(() => {
            setSymbolsError(true)
        })
    }, []);

    useEffect(() => {
        setSymbol_(symbol)
    }, [symbol]);

    if (symbolsError) {
        return (
            <div className="dashboard">
                <div>Error while loading symbols. Reload page.</div>
            </div>
        )
    }

    if (symbols === null) {
        return (
            <div className="dashboard">
                <div>Loading symbols</div>
            </div>
        )
    }

    return (

        <div className="dashboard">
            <h1>Realtime plot: {symbol_ ? symbol_ : 'choose symbol'}</h1>
            <Select
                value={symbols.filter(option => option.value === symbol_)}
                onChange={symbol => navigate(`/${symbol.value}`)}
                options={symbols}
            />
            {symbol_ ? <RealtimePlot symbol={symbol_} height={640}/> : ''}
        </div>
    )
}

