import React, { useState, useEffect, useCallback } from 'react';
import {
    Container, Paper, Typography, Box, TextField, MenuItem, FormControl, InputLabel, Select, Chip, OutlinedInput,
    Button, Modal, TableContainer, Table, TableHead, TableBody, TableRow, TableCell, IconButton, Card, CardContent, Divider, Grid2
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import CloseIcon from '@mui/icons-material/Close';
import BarChartIcon from '@mui/icons-material/BarChart';
import DownloadIcon from '@mui/icons-material/Download';

function ReportPage() {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [shelter, setShelter] = useState([]);
    const [suppliesUsed, setSuppliesUsed] = useState([]);
    const [staffInvolved, setStaffInvolved] = useState([]);
    const [animalsInvolved, setAnimalsInvolved] = useState([]);

    const [shelterList, setShelterList] = useState([]);
    const [suppliesList, setSuppliesList] = useState([]);
    const [staffList, setStaffList] = useState([]);
    const [animalsList, setAnimalsList] = useState([]);

    // State for care records and statistics
    const [careRecords, setCareRecords] = useState([]);
    const [statistics, setStatistics] = useState({});
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [loading, setLoading] = useState(false);

    const fetchAllData = useCallback(async () => {
        try {
            setLoading(true);
            const [animalResponse, staffResponse, supplyResponse, shelterResponse] = await Promise.all([
                fetch('/api/animals'),
                fetch('/api/staff'),
                fetch('/api/supplies'),
                fetch('/api/shelters')
            ]);

            // Parse JSON data from responses
            const animalData = await animalResponse.json();
            const staffData = await staffResponse.json();
            const suppliesData = await supplyResponse.json();
            const shelterData = await shelterResponse.json();

            const animals = animalData.map(
                data => ({
                    id: data[0],
                    name: data[1],
                    species: data[2],
                    shelterId: data[3]
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
                    id: data[0],
                    name: data[1],
                    quantity: data[2],
                    shelterId: data[3]
                })
            );
            const shelters = shelterData.map(
                data => ({
                    id: data[0],
                    name: data[1],
                    capacity: data[2],
                    location: data[3],
                    phoneNumber: data[4],
                    email: data[5]
                })
            );

            setAnimalsList(animals);
            setStaffList(staff);
            setSuppliesList(supplies);
            setShelterList(shelters);
            setLoading(false);

        } catch (error) {
            console.error('Error fetching data:', error);
            setLoading(false);
        }
    }, []);

    // Add useEffect to call fetchAllData on component mount
    useEffect(() => {
        fetchAllData();
    }, [fetchAllData]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const reportResponse = await fetch('/api/report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    startDate,
                    endDate,
                    shelterIds: shelter.map(shelterName => shelterList.find(shelter => shelter.name === shelterName)?.id),
                    supplyIds: suppliesUsed.map(supplyName => suppliesList.find(supply => supply.name === supplyName)?.id),
                    staffIds: staffInvolved.map(staffName => staffList.find(staff => staff.name === staffName)?.id),
                    animalIds: animalsInvolved.map(animalName => animalsList.find(animal => animal.name === animalName)?.id),
                })
            });

            const reportData = await reportResponse.json();

            // Set the care records and statistics
            setCareRecords(reportData.care_records || []);
            setStatistics(reportData.statistics || {});

            // Open the modal to display the results
            setIsModalOpen(true);
        } catch (error) {
            console.error('Error generating report:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const ITEM_HEIGHT = 48;
    const ITEM_PADDING_TOP = 8;
    const MenuProps = {
        PaperProps: {
            style: {
                maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
                width: 250,
            },
        },
    };

    const modalStyle = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '90%',
        maxWidth: '1200px',
        maxHeight: '90vh',
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
        borderRadius: 2,
        overflow: 'auto'
    };

    return (
        <Container maxWidth="md" sx={{ mt: 4 }}>
            <Paper elevation={3} sx={{ p: 4 }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Shelter Activity Report
                </Typography>

                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
                    <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
                        <TextField
                            label="Start Date"
                            type="date"
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />

                        <TextField
                            label="End Date"
                            type="date"
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            fullWidth
                            InputLabelProps={{ shrink: true }}
                        />
                    </Box>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                        <InputLabel id="shelter-select-label">Shelter</InputLabel>
                        <Select
                            labelId="shelter-select-label"
                            id="shelter-select"
                            value={shelter}
                            multiple
                            label="Shelter"
                            onChange={(e) => setShelter(e.target.value)}
                            input={<OutlinedInput id="select-multiple-shelters" label="Shelters" />}
                            renderValue={(selected) => (
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                    {selected.map((value) => (
                                        <Chip key={value} label={value} />
                                    ))}
                                </Box>
                            )}
                            MenuProps={MenuProps}
                        >
                            {shelterList.map((shelterItem) => (
                                <MenuItem key={shelterItem.id} value={shelterItem.name}>
                                    {shelterItem.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                        <InputLabel id="supplies-select-label">Supplies Used</InputLabel>
                        <Select
                            labelId="supplies-select-label"
                            id="supplies-select"
                            multiple
                            value={suppliesUsed}
                            onChange={(e) => setSuppliesUsed(e.target.value)}
                            input={<OutlinedInput id="select-multiple-supplies" label="Supplies Used" />}
                            renderValue={(selected) => (
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                    {selected.map((value) => (
                                        <Chip key={value} label={value} />
                                    ))}
                                </Box>
                            )}
                            MenuProps={MenuProps}
                        >
                            {suppliesList.map((supply) => (
                                <MenuItem key={supply.id} value={supply.name}>
                                    {supply.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                        <InputLabel id="staff-select-label">Staff Involved</InputLabel>
                        <Select
                            labelId="staff-select-label"
                            id="staff-select"
                            multiple
                            value={staffInvolved}
                            onChange={(e) => setStaffInvolved(e.target.value)}
                            input={<OutlinedInput id="select-multiple-staff" label="Staff Involved" />}
                            renderValue={(selected) => (
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                    {selected.map((value) => (
                                        <Chip key={value} label={value} />
                                    ))}
                                </Box>
                            )}
                            MenuProps={MenuProps}
                        >
                            {staffList.map((staffMember) => (
                                <MenuItem key={staffMember.id} value={staffMember.name}>
                                    {staffMember.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <FormControl fullWidth sx={{ mb: 3 }}>
                        <InputLabel id="animals-select-label">Animals Involved</InputLabel>
                        <Select
                            labelId="animals-select-label"
                            id="animals-select"
                            multiple
                            value={animalsInvolved}
                            onChange={(e) => setAnimalsInvolved(e.target.value)}
                            input={<OutlinedInput id="select-multiple-animals" label="Animals Involved" />}
                            renderValue={(selected) => (
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                    {selected.map((value) => (
                                        <Chip key={value} label={value} />
                                    ))}
                                </Box>
                            )}
                            MenuProps={MenuProps}
                        >
                            {animalsList.map((animal) => (
                                <MenuItem key={animal.id} value={animal.name}>
                                    {animal.name}
                                </MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                        <Button
                            type="submit"
                            variant="contained"
                            color="primary"
                            size="large"
                            disabled={loading}
                        >
                            {loading ? 'Generating...' : 'Generate Report'}
                        </Button>
                    </Box>
                </Box>
            </Paper>


            <Modal
                open={isModalOpen}
                onClose={handleCloseModal}
                aria-labelledby="report-results-modal"
                aria-describedby="modal-displaying-report-results"
            >
                <Box sx={modalStyle}>

                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                        <Typography variant="h5" component="h2" sx={{ fontWeight: 'bold' }}>
                            Report Results
                        </Typography>
                        <Box>
                            <IconButton onClick={handleCloseModal}>
                                <CloseIcon />
                            </IconButton>
                        </Box>
                    </Box>

                    <Typography variant="h6" component="h3" sx={{ mb: 2 }}>
                        Care Records
                    </Typography>

                    <TableContainer
                        component={Paper}
                        sx={{
                            boxShadow: 3,
                            borderRadius: 2,
                            overflow: 'hidden'
                        }}
                    >
                        <Table sx={{ minWidth: 650 }}>
                            <TableHead sx={{ bgcolor: 'primary.light' }}>
                                <TableRow>
                                    <TableCell sx={{ fontWeight: 'bold', color: 'primary.contrastText' }}>ID</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold', color: 'primary.contrastText' }}>Shelter</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold', color: 'primary.contrastText' }}>Animal</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold', color: 'primary.contrastText' }}>Staff Member</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold', color: 'primary.contrastText' }}>Date</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold', color: 'primary.contrastText' }}>Notes</TableCell>
                                    <TableCell sx={{ fontWeight: 'bold', color: 'primary.contrastText' }}>Supplies</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {careRecords.length > 0 ? (
                                    careRecords.map((record, index) => (
                                        <TableRow
                                            key={record.record_id}
                                            sx={{
                                                '&:hover': { bgcolor: 'action.hover' },
                                                bgcolor: index % 2 === 0 ? 'background.default' : 'background.paper'
                                            }}
                                        >
                                            <TableCell>{record.record_id}</TableCell>
                                            <TableCell>{record.shelter_name}</TableCell>
                                            <TableCell>{record.animal_name}</TableCell>
                                            <TableCell>{record.staff_name}</TableCell>
                                            <TableCell>{new Date(record.date.concat("T12:00:00")).toLocaleDateString()}</TableCell>
                                            <TableCell
                                                sx={{
                                                    maxWidth: '200px',
                                                    overflow: 'hidden',
                                                    textOverflow: 'ellipsis',
                                                    whiteSpace: 'nowrap',
                                                }}
                                            >
                                                {record.notes}
                                            </TableCell>
                                            <TableCell>
                                                {record.supplies && record.supplies.length > 0 ? (
                                                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                                        {record.supplies.map((supply) => (
                                                            <Chip
                                                                key={supply.supply_id}
                                                                label={`${supply.supply_name} (${supply.supply_quantity})`}
                                                                size="small"
                                                                variant="outlined"
                                                                color="primary"
                                                                sx={{ m: 0.25 }}
                                                            />
                                                        ))}
                                                    </Box>
                                                ) : (
                                                    <Typography variant="body2" color="text.secondary">
                                                        No supplies used
                                                    </Typography>
                                                )}
                                            </TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    <TableRow>
                                        <TableCell colSpan={7} align="center" sx={{ py: 4 }}>
                                            <Typography variant="body1" color="text.secondary">
                                                No care records found matching your criteria.
                                            </Typography>
                                        </TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>

                    <Divider sx={{ my: 3 }} />

                    {careRecords.length > 0 && (
                        <Paper elevation={2} sx={{ p: 2, mb: 4, bgcolor: '#f8f9fa' }}>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                                <BarChartIcon sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="h6" component="h3">
                                    Key Statistics
                                </Typography>
                            </Box>

                            <Grid2 container className='justify-center' spacing={3}>
                                {Object.entries(statistics).map(([statName, statData]) => (
                                    <Grid2 item xs={12} sm={6} md={4} key={statName}>
                                        <Card variant="outlined">
                                            <CardContent>
                                                <Typography color="textSecondary" gutterBottom>
                                                    {statName}
                                                </Typography>
                                                <Typography variant="h6" component="div">
                                                    {statData.value}
                                                </Typography>
                                                {statData.count && (
                                                    <Typography variant="body2" color="textSecondary">
                                                        Count: {statData.count}
                                                    </Typography>
                                                )}
                                            </CardContent>
                                        </Card>
                                    </Grid2>
                                ))}
                            </Grid2>
                        </Paper>
                    )}

                </Box>
            </Modal>
        </Container>
    );
}

export default ReportPage;