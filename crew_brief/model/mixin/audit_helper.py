import sqlalchemy as sa

class AuditHelper:
    """
    Helpful functions for auditing the history of records.
    """

    def __init__(self, model_class):
        self.model_class = model_class

    def get_full_history(self, session, record_id, include_operation_details=True):
        """
        Get complete history for a record with operation details
        """
        history_class = self.model_class._history_class
        pk_column = (
            f'{self.model_class.__tablename__}'
            f'_{list(self.model_class.__table__.primary_key.columns)[0].name}'
        )

        query = (
            sa.select(history_class)
            .where(getattr(history_class, pk_column) == record_id)
            .order_by(history_class.operation_timestamp.desc())
        )
        if include_operation_details:
            query = query.join(OperationTypeModel)

        return session.scalars(query).all() #query.all()

    def get_record_at_timestamp(self, session, record_id, timestamp):
        """
        Get the state of a record at a specific timestamp
        """
        history_class = self.model_class._history_class
        pk_column = (
            f'{self.model_class.__tablename__}'
            f'_{list(self.model_class.__table__.primary_key.columns)[0].name}'
        )
        # Get the first history record on or before the given timestamp.
        query = (
            sa.select(history_class)
            .where(
                getattr(history_class, pk_column) == record_id,
                history_class.operation_timestamp <= timestamp,
            )
            .order_by(
                history_class.operation_timestamp.desc(),
            )
        )
        return session.scalars(query).first()

    def get_changes_by_operation(
        self,
        session,
        operation_type,
        start_date = None,
        end_date = None,
    ):
        """
        Get all changes of a specific operation type
        """
        history_class = self.model_class._history_class
        query = (
            sa.select(history_class)
            .where(history_class.operation_type_id == operation_type.value)
        )

        if start_date:
            query = query.where(history_class.operation_timestamp >= start_date)
        if end_date:
            query = query.where(history_class.operation_timestamp <= end_date)

        query = query.order_by(history_class.operation_timestamp.desc())

        return session.scalars(query).all()

    def get_audit_trail(self, session, record_id):
        """
        Get a formatted audit trail for a record
        """
        history_records = self.get_full_history(session, record_id)

        audit_trail = []
        for record in history_records:
            audit_entry = {
                'timestamp': record.operation_timestamp,
                'operation': record.operation_type.name,
                'user': record.operation_user or 'System',
                'changes': {}
            }

            # Add the actual field values
            for column in self.model_class.__table__.columns:
                if not column.primary_key and hasattr(record, column.name):
                    audit_entry['changes'][column.name] = getattr(record, column.name)

            audit_trail.append(audit_entry)

        return audit_trail
