import { Router } from 'express';
import { convertToJSON } from '../controllers/diagramController.js';

const router = Router();

router.post('/convert', convertToJSON);

export default router;
