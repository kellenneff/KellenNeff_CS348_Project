import React, { useState, useEffect } from 'react';
import {
    Modal, Typography, IconButton, TextField, Autocomplete, Popper,
    Button, Snackbar, Alert
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import SupplyUsage from './SupplyUsage';

const AddCareRecordModal = ({ open, handleClose, animalList = [], staffList = [], supplyList = [], shelterList = [], onRecordAdd }) => {
    const [filteredAnimals, setFilteredAnimals] = useState(animalList);
    const [filteredStaff, setFilteredStaff] = useState(staffList);
    const [filteredSupplies, setFilteredSupplies] = useState(supplyList);
    const [selectedAnimal, setSelectedAnimal] = useState(null);
    const [selectedStaff, setSelectedStaff] = useState(null);
    const [selectedShelter, setSelectedShelter] = useState(null);
    const [date, setDate] = useState('');
    const [notes, setNotes] = useState('');
    const [supplies, setSupplies] = useState(supplyList);
    const [selectedSupplies, setSelectedSupplies] = useState([]);

    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState('success');



    const addSupplyUsage = () => {
        setSelectedSupplies([...selectedSupplies, { supply: null, quantity: 1 }]);
    };

    const updateSupplyUsage = (index, field, value) => {
        const newSupplies = [...selectedSupplies];
        newSupplies[index][field] = value;
        setSelectedSupplies(newSupplies);
        console.log(selectedSupplies);

        const usedSupplyIds = newSupplies.filter(item => item.supply !== null)
            .map(item => item.supply.supply_id)

        let supplies = [];
        if (selectedShelter !== null) {
            supplies = supplyList.filter(supply => supply.shelter_id === selectedShelter.id);
        } else {
            supplies = supplyList;
        }
        const filteredAvailableSupplies = supplies.filter(
            supply => !usedSupplyIds.includes(supply.supply_id)
        );

        setFilteredSupplies(filteredAvailableSupplies);
    }

    const removeSupplyUsage = (index) => {
        const newSupplies = selectedSupplies.filter((supply, i) => i !== index);

        setSelectedSupplies(newSupplies);

        const usedSupplyIds = newSupplies.filter(item => item.supply !== null)
            .map(item => item.supply.supply_id)

        let supplies = [];
        if (selectedShelter !== null) {
            supplies = supplyList.filter(supply => supply.shelter_id === selectedShelter.id);
        } else {
            supplies = supplyList;
        }
        const filteredAvailableSupplies = supplies.filter(
            supply => !usedSupplyIds.includes(supply.supply_id)
        );

        setFilteredSupplies(filteredAvailableSupplies);
    }


    const handleSubmit = async () => {
        if (!selectedShelter || !selectedAnimal || !selectedStaff || !date) {
            setSnackbarMessage('Please fill in all required fields');
            setSnackbarSeverity('error');
            setOpenSnackbar(true);
            return;
        }

        const invalidSupplies = selectedSupplies.some(supply => !supply.supply || supply.quantity < 1);
        if (invalidSupplies) {
            setSnackbarMessage('Please fill in all supply fields');
            setSnackbarSeverity('error');
            setOpenSnackbar(true);
            return;
        }

        try {
            const careRecordResponse = await fetch('/api/care_records', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    animal_id: selectedAnimal.id,
                    staff_id: selectedStaff.id,
                    date: date,
                    notes: notes || null
                })
            });
            if (!careRecordResponse.ok) {
                throw new Error('Failed to add care record');
            }

            const careRecordData = await careRecordResponse.json();
            const careRecordId = careRecordData.record_id;

            
            //console.log(careRecordId)

            const supplyUsagesResponse = await fetch('/api/supply_usage', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(
                    selectedSupplies.map(supply => ({
                        supply_id: supply.supply.supply_id,
                        quantity: supply.quantity,
                        care_record_id: careRecordId
                    }))
                )
            });

            if (!supplyUsagesResponse.ok) {
                throw new Error('Failed to add supply usage');
            }

            if (onRecordAdd) {
                onRecordAdd();
            }
            onClose();
        } catch (error) {
            console.error("Error creating care record:", error);
            setSnackbarMessage('Failed to add care record');
            setSnackbarSeverity('error');
            setOpenSnackbar(true);
        }

    };

    const handleSnackbarClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpenSnackbar(false);
    };

    const onClose = () => {
        setSelectedAnimal(null);
        setSelectedStaff(null);
        setSelectedSupplies([]);
        setDate('');
        setNotes('');
        setSelectedShelter(null);
        handleClose();
    }

    const disableFlipUp = (props) => (
        <Popper
            {...props}
            modifiers={[
                {
                    name: 'flip',
                    enabled: false,
                },
                {
                    name: 'preventOverflow',
                    enabled: false,
                }
            ]}
        />
    );

    const handleAnimalChange = (e) => {
        const animalId = e ? e.id : '';
        setSelectedAnimal(e);
    }

    const handleStaffChange = (e) => {
        const staffId = e ? e.id : '';
        setSelectedStaff(e);
    }

    const handleShelterChange = (e) => {
        const shelterId = e ? e.id : '';
        if (shelterId !== selectedShelter?.id) {
            setSelectedAnimal(null);
            setSelectedStaff(null);
            setSelectedSupplies([]);

            if (shelterId !== '') {
                const animals = animalList.filter(animal => animal.shelterId === shelterId);
                setFilteredAnimals(animals);
                const staff = staffList.filter(staff => staff.shelterId === shelterId);
                setFilteredStaff(staff);
                const supplies = supplyList.filter(supply => supply.shelter_id === shelterId);
                setFilteredSupplies(supplies);
                console.log(filteredSupplies);
            }

            setSelectedShelter(e);
        }
    }


    return (
        <>
            <Modal
                open={open}
                onClose={onClose}
                aria-labelledby="add-care-record-modal"
            >
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[600px] max-w-[90vw] max-h-[90vh] overflow-auto bg-white rounded-lg shadow-lg outline-none">

                    <div className="flex justify-between items-center bg-blue-600 text-white p-4 rounded-t-lg">
                        <Typography variant="h5" sx={{ fontWeight: 'bold' }}>
                            Add New Care Record
                        </Typography>
                        <IconButton onClick={onClose} size="small" sx={{ color: 'white' }}>
                            <CloseIcon />
                        </IconButton>
                    </div>


                    <div className="p-6">

                        <div className='mb-6'>
                            <Typography variant='subtitle1' className='mb-1 font-medium'>
                                Shelter
                            </Typography>
                            <Autocomplete
                                disablePortal
                                value={selectedShelter}
                                onChange={(event, newValue) => handleShelterChange(newValue)}
                                options={shelterList}
                                slots={{ Popper: disableFlipUp }}
                                isOptionEqualToValue={(option, value) => option.id === value?.id}
                                getOptionLabel={(option) => option?.name || ''}
                                renderInput={(params) => (
                                    <TextField
                                        {...params}
                                        label='Select Shelter'
                                        fullWidth
                                        required
                                    />
                                )}
                                renderOption={(props, option) => {
                                    const { key, ...optionProps } = props;
                                    return (
                                        <li key={key} {...optionProps}>
                                            <div className='py-3 px-4'>
                                                <Typography variant='body1'>{option.name}</Typography>
                                            </div>
                                        </li>
                                    );
                                }}
                            />
                        </div>
                        {selectedShelter ? (
                            <div>

                                <div className="mb-6">
                                    <Typography variant="subtitle1" className="mb-1 font-medium">
                                        Animal
                                    </Typography>
                                    <Autocomplete
                                        disablePortal
                                        value={selectedAnimal}
                                        onChange={(event, newValue) => handleAnimalChange(newValue)}
                                        options={filteredAnimals}
                                        slots={{ Popper: disableFlipUp }}
                                        getOptionLabel={(option) => option.name || ''}
                                        renderInput={(params) => (
                                            <TextField
                                                {...params}
                                                label="Select Animal"
                                                fullWidth
                                                required
                                            />
                                        )}
                                        renderOption={(props, option) => {
                                            const { key, ...optionProps } = props;
                                            return (
                                                <li key={key} {...optionProps}>
                                                    <div className="py-3 px-4">
                                                        <Typography variant="body1">{option.name}</Typography>
                                                        <Typography variant="body2" color="text.secondary">
                                                            {option.species}
                                                        </Typography>
                                                    </div>
                                                </li>
                                            );
                                        }}
                                    />
                                </div>

                                <div className="mb-6">
                                    <Typography variant="subtitle1" className="mb-1 font-medium">
                                        Staff Member
                                    </Typography>
                                    <Autocomplete
                                        disablePortal
                                        value={selectedStaff}
                                        onChange={(event, newValue) => handleStaffChange(newValue)}
                                        options={filteredStaff}
                                        slots={{ Popper: disableFlipUp }}
                                        getOptionLabel={(option) => option.name || ''}
                                        renderInput={(params) => (
                                            <TextField
                                                {...params}
                                                label="Select Staff"
                                                fullWidth
                                                required
                                            />
                                        )}
                                        renderOption={(props, option) => {
                                            const { key, ...optionProps } = props;
                                            return (
                                                <li key={key} {...optionProps}>
                                                    <div className="py-3 px-4">
                                                        <Typography variant="body1">{option.name}</Typography>
                                                        <Typography variant="body2" color="text.secondary">
                                                            {option.role}
                                                        </Typography>
                                                    </div>
                                                </li>
                                            );
                                        }}
                                    />
                                </div>

                                <div className="mb-6">
                                    <Typography variant="subtitle1" className="mb-1 font-medium">
                                        Date
                                    </Typography>
                                    <TextField
                                        type="date"
                                        value={date}
                                        onChange={(e) => setDate(e.target.value)}
                                        fullWidth
                                        required
                                        slotProps={{ inputLabel: { shrink: true } }}
                                    />
                                </div>

                                <div className="mb-6">
                                    <Typography variant="subtitle1" className="mb-1 font-medium">
                                        Treatment Notes
                                    </Typography>
                                    <TextField
                                        multiline
                                        rows={4}
                                        value={notes}
                                        onChange={(e) => setNotes(e.target.value)}
                                        placeholder="Enter details about the treatment provided..."
                                        fullWidth
                                        variant="outlined"
                                    />
                                </div>

                                <div className='mb-6'>
                                    <Typography varient='h6' className='mb-2 font-medium'>
                                        Supplies Used
                                    </Typography>

                                    {selectedSupplies.map((supply, index) => (
                                        <SupplyUsage
                                            key={index}
                                            supplyList={filteredSupplies}
                                            supply={supply.supply}
                                            quantity={supply.quantity}
                                            initialSupply={supply.name}
                                            initialQuantity={supply.quantity}
                                            onSupplyChange={(supply) => updateSupplyUsage(index, 'supply', supply)}
                                            onQuantityChange={(quantity) => updateSupplyUsage(index, 'quantity', quantity)}
                                            onDelete={() => removeSupplyUsage(index)}
                                        />
                                    ))}

                                    <Button
                                        variant='outlined'
                                        onClick={addSupplyUsage}
                                        className='mt-2'
                                    >Add Supply</Button>

                                </div>
                            </div>
                        ) : (
                            <div className='flex items-center justify-center h-32'></div>
                        )}
                    </div>

                    <div className="p-4 bg-gray-100 flex justify-end gap-4 rounded-b-lg">
                        <Button
                            variant="outlined"
                            onClick={onClose}
                        >
                            Cancel
                        </Button>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleSubmit}
                        >
                            Save Record
                        </Button>
                    </div>
                </div>
            </Modal>

            <Snackbar
                open={openSnackbar}
                autoHideDuration={6000}
                onClose={handleSnackbarClose}
                anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            >
                <Alert
                    onClose={handleSnackbarClose}
                    severity={snackbarSeverity}
                    sx={{ width: '100%' }}
                >
                    {snackbarMessage}
                </Alert>
            </Snackbar>

        </>
    );
};


export default AddCareRecordModal;