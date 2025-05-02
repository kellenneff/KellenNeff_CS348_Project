import React, { useEffect, useState, useCallback } from 'react';
import {
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
    Paper, IconButton, Button, Typography, Chip, Modal, Box
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import AddIcon from '@mui/icons-material/Add';
import MedicationIcon from '@mui/icons-material/Medication';
import AddCareRecordModal from './components/AddRecordModal.jsx';
import EditRecordModal from './components/EditRecordModal.jsx';
import { Add } from '@mui/icons-material';

function ModifyPage() {
    const [addModalOpen, setAddModalOpen] = useState(false);
    const [editModalOpen, setEditModalOpen] = useState(false);
    const [animalList, setAnimalList] = useState([]);
    const [staffList, setStaffList] = useState([]);
    const [suppliesList, setSuppliesList] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [careRecords, setCareRecords] = useState([]);
    const [shelterList, setShelterList] = useState([]);
    const [selectedRecord, setSelectedRecord] = useState(null);

    const fetchAllData = useCallback(async () => {
        try {
            const [recordsResponse, animalResponse, staffResponse, supplyResponse, shelterResponse] = await Promise.all([
                fetch('/api/care_records_info'),
                fetch('/api/animals'),
                fetch('/api/staff'),
                fetch('/api/supplies_with_inventory'),
                fetch('/api/shelters')
            ]);

            const recordsData = await recordsResponse.json();
            const animalsData = await animalResponse.json();
            const staffData = await staffResponse.json();
            const suppliesData = await supplyResponse.json();
            const shelterData = await shelterResponse.json();

            console.log('Supplies data', suppliesData);

            const animals = animalsData.map(
                data => ({
                    id: data[0],
                    name: data[1],
                    species: data[2],
                    shelterId: data[3],
                })
            );
            const staff = staffData.map(
                data => ({
                    id: data[0],
                    name: data[1],
                    email: data[2],
                    role: data[3],
                    shelterId: data[4]
                })
            );
            const supplies = suppliesData.map(
                data => ({
                    supply_id: data[0],
                    name: data[1],
                    quantity: data[2],
                    shelter_id: data[3]
                })
            );
            const shelters = shelterData.map(
                data => ({
                    id: data[0],
                    name: data[1],
                    capacity: data[2],
                    location: data[3],
                    phone_number: data[4],
                    email: data[5]
                })
            );

            setCareRecords(recordsData);
            setAnimalList(animals);
            setStaffList(staff);
            setSuppliesList(supplies);
            setShelterList(shelters);
            setIsLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchAllData();
    }, [fetchAllData]);



    const handleRefreshRecords = () => {
        fetchAllData();
    };
    
    const handleDelete = async (recordId) => {
        if (!recordId) return;

        try {
            const response = await fetch(`/api/care_records/${recordId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to delete record');
            }

            handleRefreshRecords();
        }
        catch (error){
            console.error('Error deleting record:', error);
            throw new Error('Failed to delete record');
        }
    };

    const handleEdit = (recordId) => {
        const record = careRecords.find((r) => r.record_id === recordId);
        setSelectedRecord(record);
        setEditModalOpen(true);
    };

    const handleAdd = () => {
        setAddModalOpen(true);
    };

    const handleViewSupplies = (recordId) => {
        console.log(`View supplies for record ID: ${recordId}`);
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <Typography variant="h6">Loading...</Typography>
            </div>
        )
    }

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <div className="flex justify-between items-center mb-6">
                <Typography variant="h4" component="h1" className="text-blue-700 font-bold">
                    Animal Care Records
                </Typography>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<AddIcon />}
                    onClick={handleAdd}
                >
                    New Care Record
                </Button>
            </div>

            <AddCareRecordModal
                open={addModalOpen}
                handleClose={() => setAddModalOpen(false)}
                animalList={animalList}
                staffList={staffList}
                supplyList={suppliesList}
                shelterList={shelterList}
                onRecordAdd={handleRefreshRecords}
            />

            <EditRecordModal
                open={editModalOpen}
                handleClose={() => setEditModalOpen(false)}
                careRecord={selectedRecord}
                animalList={animalList}
                staffList={staffList}
                supplyList={suppliesList}
                shelterList={shelterList}
                onRecordAdd={handleRefreshRecords}
            />

            <Paper className="mb-4 p-4 bg-blue-50">
                <Typography variant="body1">
                    Manage treatment records for animals, including staff assignments and medical supplies used.
                </Typography>
            </Paper>

            <TableContainer component={Paper} className="shadow-lg">
                <Table>
                    <TableHead className="bg-blue-100">
                        <TableRow>
                            <TableCell className="font-bold">ID</TableCell>
                            <TableCell className='font-bold'>Shelter</TableCell>
                            <TableCell className="font-bold">Animal</TableCell>
                            <TableCell className="font-bold">Staff Member</TableCell>
                            <TableCell className="font-bold">Date</TableCell>
                            <TableCell className="font-bold">Notes</TableCell>
                            <TableCell className="font-bold">Supplies</TableCell>
                            <TableCell className="font-bold" align="center">Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {careRecords.length > 0 ? (
                            careRecords.map((record) => (
                                <TableRow key={record.record_id} className="hover:bg-gray-50">
                                    <TableCell>{record.record_id}</TableCell>
                                    <TableCell>{record.shelter_name}</TableCell>
                                    <TableCell>{record.animal_name}</TableCell>
                                    <TableCell>{record.staff_name}</TableCell>
                                    <TableCell>{new Date(record.date.concat("T12:00:00")).toLocaleDateString()}</TableCell>
                                    <TableCell className="max-w-xs truncate">{record.notes}</TableCell>
                                    <TableCell>
                                        {record.supplies && record.supplies.length > 0 ? (
                                            <div className="flex flex-col space-y-1">
                                                {record.supplies.map((supply) => (
                                                    <Chip
                                                        key={supply.supply_id}
                                                        label={`${supply.supply_name} (${supply.supply_quantity})`}
                                                        size="small"
                                                        variant="outlined"
                                                        color="primary"
                                                        className="mr-1 mb-1"
                                                    />
                                                ))}
                                            </div>
                                        ) : (
                                            <Typography variant="body2" color="textSecondary">
                                                No supplies used
                                            </Typography>
                                        )}
                                    </TableCell>
                                    <TableCell align="center">
                                        <div className="flex justify-center space-x-2">
                                            <IconButton
                                                color="primary"
                                                size="small"
                                                onClick={() => handleEdit(record.record_id)}
                                            >
                                                <EditIcon />
                                            </IconButton>
                                            <IconButton
                                                color="error"
                                                size="small"
                                                onClick={() => handleDelete(record.record_id)}
                                            >
                                                <DeleteIcon />
                                            </IconButton>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ))
                        ) : (
                            <TableRow>
                                <TableCell colSpan={7} className="text-center py-8">
                                    <Typography variant="body1" color="textSecondary">
                                        No care records found. Add a new record to get started.
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>

            {/* Loading state example */}
            {false && (
                <div className="flex justify-center my-4">
                    <Typography>Loading records...</Typography>
                </div>
            )}
        </div>
    );
}

export default ModifyPage;