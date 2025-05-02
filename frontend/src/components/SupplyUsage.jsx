import React from 'react';
import { Autocomplete, TextField, IconButton, Typography } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

const SupplyUsage = ({ 
    supplyList, 
    supply, 
    quantity, 
    onSupplyChange, 
    onQuantityChange,
    maxQuantity, 
    onDelete 
}) => {
    const handleSupplyChange = (event, newValue) => {
        onSupplyChange(newValue);
    }

    const handleQuantityChange = (event) => {
        const newQuantity = parseInt(event.target.value, 10);
        const maxQuantity = supplyList.find(s => s.id === supply.id)?.quantity || 0;
        const validatedQuantity = Math.max(
            1, 
            Math.min(newQuantity, maxQuantity)
        );
        onQuantityChange(validatedQuantity);
    }

    return (
        <div className='flex items-center gap-4 mb-4'>
            <Autocomplete
                disablePortal
                value={supply}
                onChange={handleSupplyChange}
                options={supplyList}
                isOptionEqualToValue={(option, value) => option?.id === value?.id}
                getOptionLabel={(option) => option?.name || ''}
                renderInput={(params) => (
                    <TextField
                        {...params}
                        label="Select Supply"
                        fullWidth
                        required
                    />
                )}
                renderOption={(props, option) => {
                    const { key, ...optionProps } = props;
                    return (
                        <li key={option.id} {...optionProps}>
                            <div className='py-3 px-4'>
                                <Typography variant='body1'>{option.name}</Typography>
                                <Typography variant='body2' color='text.secondary'>
                                    Available: {option.quantity}
                                </Typography>
                            </div>
                        </li>
                    );
                }}
                className='flex-grow'
                sx={{ marginRight: 2 }}
            />
            <TextField
                type='number'
                label='Quantity'
                value={quantity}
                onChange={handleQuantityChange}
                inputProps={{ 
                    min: 1, 
                    max: supply ? supply.quantity : 0 
                }}
                className='w-32'
            />
            <IconButton onClick={onDelete} color='error'>
                <DeleteIcon />
            </IconButton>
        </div>
    );
};

export default SupplyUsage;